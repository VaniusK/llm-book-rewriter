from file_handler import FileHandler
from starlette.staticfiles import StaticFiles
import logging
import asyncio
from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Form, Request
from fastapi.responses import FileResponse
import zipfile
import io
import os
from pathlib import Path
import json
from book_processor import BookProcessor
from config import load_config, deep_merge_dicts, config_local_filename
# pyrefly: ignore [missing-import]
import diff_match_patch as dmp_module
import time
import re
from contextlib import asynccontextmanager


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.getLogger('google_genai').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)

tasks: dict[str, (asyncio.Task, Path, Path)] = {}


MAX_FILE_SIZE = 1024 * 1024 * 10
SUPPORTED_EXTENSIONS = ["fb2", "txt", "docx"]
OUTPUT_DIR = Path("output_books")
INPUT_DIR = Path("input_books")
INPUT_DIR.mkdir(parents=True, exist_ok=True)
PROCESSING_TIMEOUT_SECONDS = 3600
MAX_CONCURRENT_TASKS_PER_IP = 3
MAX_CONCURRENT_TASKS = 100

def remove_file(path: Path):
    if os.path.exists(path):
        os.remove(path)

def clean_directories():
    for file in Path(".").iterdir():
        if file.suffix[1:] == "zip":
            remove_file(file)
    for file in Path(INPUT_DIR).iterdir():
        remove_file(file)
    for file in Path(OUTPUT_DIR).iterdir():
        remove_file(file)

async def cleanup_task():
    while True:
        tasks_list = list(tasks.keys())
        for task_id in tasks_list:
            if time.time() - tasks[task_id][6] > PROCESSING_TIMEOUT_SECONDS:
                remove_file(task_id + ".zip")
                remove_file(tasks[task_id][1])
                remove_file(OUTPUT_DIR / tasks[task_id][2])
                tasks.pop(task_id)
        await asyncio.sleep(PROCESSING_TIMEOUT_SECONDS)

clean_directories()

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(cleanup_task())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)


@app.post("/process/file")
async def process_file(request: Request, config_str: str = Form(...), file: UploadFile = File(...)):
    config_tmp = json.loads(config_str)
    config = deep_merge_dicts(config_tmp, load_config(Path(config_local_filename)))
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Разрешены только файлы с расширением .zip")
    client_ip = request.client.host
    if len([task_id for task_id in tasks if tasks[task_id][7] == client_ip]) > MAX_CONCURRENT_TASKS:
        raise HTTPException(status_code=429, detail="Превышен лимит на количество одновременных задач от одного IP")
    if len(tasks) > MAX_CONCURRENT_TASKS:
        raise HTTPException(status_code=429, detail="Сервер перегружен")
    zip_properties = await file.read()
    original_filename = None
    id = str(uuid4())
    with zipfile.ZipFile(io.BytesIO(zip_properties)) as z:
        if len(z.namelist()) != 1:
            raise HTTPException(status_code=400, detail="Архив должен содержать только один файл")
        for info in z.infolist():
            if info.file_size > MAX_FILE_SIZE:
                raise HTTPException(status_code=400, detail="Превышен максимальный размер файла")
            
            original_filename = Path(info.filename)
            ext = original_filename.suffix[1:]
            info.filename = id + "." + ext
            if ext not in SUPPORTED_EXTENSIONS:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Архив содержит запрещенный файл: {original_filename}"
                    )
            z.extract(info, path=INPUT_DIR)
        book_processor = BookProcessor(config, ext)
        input_file = INPUT_DIR / Path(id + "." + ext)
        output_file = Path(f"{id}_rewritten." + ext)
        tasks[id] = (asyncio.create_task(book_processor.process_book(input_file, output_file)), input_file, output_file, original_filename, Path(file.filename), config, time.time(), client_ip)
    return {"message": "Начата обработка файла", "task_id": id}

@app.get("/tasks/{task_id}")
async def check_task_status(task_id: str):
    if not task_id in tasks:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    return {"is_completed": tasks[task_id][0].done()}

@app.post("/tasks/{task_id}/result")
async def get_task_result(task_id: str, background_tasks: BackgroundTasks, final_text: str = Form(...)):
    if not task_id in tasks:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    if not tasks[task_id][0].done():
        raise HTTPException(status_code=400, detail="Задача ещё не завершена")

    file_handler = FileHandler(tasks[task_id][1].suffix[1:], tasks[task_id][5]).file_handler
    file_handler.insert_text(OUTPUT_DIR / tasks[task_id][2], final_text, OUTPUT_DIR / tasks[task_id][2], )
    with zipfile.ZipFile(task_id + ".zip", 'w') as z:
        z.write(OUTPUT_DIR / tasks[task_id][2], arcname=tasks[task_id][3])

    background_tasks.add_task(remove_file, task_id + ".zip")
    background_tasks.add_task(remove_file, tasks[task_id][1])
    background_tasks.add_task(remove_file, OUTPUT_DIR / tasks[task_id][2])
    background_tasks.add_task(lambda: tasks.pop(task_id))
    return FileResponse(
        path=task_id + ".zip",
        filename=tasks[task_id][4].stem + "_rewritten.zip",
        media_type="application/zip"
    )

@app.get("/tasks/{task_id}/diff")
async def get_task_diff(task_id: str):
    if not task_id in tasks:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    if not tasks[task_id][0].done():
        raise HTTPException(status_code=400, detail="Задача ещё не завершена")
    
    file_handler = FileHandler(tasks[task_id][1].suffix[1:], tasks[task_id][5]).file_handler
    original_text = file_handler.extract_text(tasks[task_id][1])
    processed_text = file_handler.extract_text(OUTPUT_DIR / tasks[task_id][2])
    pattern = re.compile(r'\w+|\s+|[^\w\s]+')
    tokens1 = pattern.findall(original_text)
    tokens2 = pattern.findall(processed_text)
    
    token_to_char = {}
    char_to_token = []
    
    START_CHAR = 0xE000 
    
    def tokens_to_chars(tokens):
        chars = []
        for token in tokens:
            if token not in token_to_char:
                token_to_char[token] = chr(START_CHAR + len(char_to_token))
                char_to_token.append(token)
            chars.append(token_to_char[token])
        return "".join(chars)
        
    chars1 = tokens_to_chars(tokens1)
    chars2 = tokens_to_chars(tokens2)
    
    dmp = dmp_module.diff_match_patch()
    diffs_chars = dmp.diff_main(chars1, chars2, False) 
    
    raw_diffs = []
    for op, text_chars in diffs_chars:
        text = "".join(char_to_token[ord(c) - START_CHAR] for c in text_chars)
        raw_diffs.append((op, text))
        
    diff_list = []
    src_idx = 0
    tgt_idx = 0
    
    i = 0
    while i < len(raw_diffs):
        op, text = raw_diffs[i]
        
        if op == 0:
            src_idx += len(text)
            tgt_idx += len(text)
            i += 1
            continue
            
        next_op = raw_diffs[i+1][0] if i + 1 < len(raw_diffs) else 0
        
        if (op == -1 and next_op == 1) or (op == 1 and next_op == -1):
            if op == -1:
                del_text = text
                ins_text = raw_diffs[i+1][1]
            else:
                ins_text = text
                del_text = raw_diffs[i+1][1]
                
            diff_list.append({
                "operation": "replace",
                "source_range": (src_idx, src_idx + len(del_text)),
                "target_range": (tgt_idx, tgt_idx + len(ins_text)),
                "text_removed": del_text,
                "text_added": ins_text
            })
            src_idx += len(del_text)
            tgt_idx += len(ins_text)
            i += 2
            
        elif op == -1:
            diff_list.append({
                "operation": "delete",
                "source_range": (src_idx, src_idx + len(text)),
                "target_range": (tgt_idx, tgt_idx),
                "text_removed": text,
                "text_added": ""
            })
            src_idx += len(text)
            i += 1
            
        elif op == 1:
            diff_list.append({
                "operation": "insert",
                "source_range": (src_idx, src_idx),
                "target_range": (tgt_idx, tgt_idx + len(text)),
                "text_removed": "",
                "text_added": text
            })
            tgt_idx += len(text)
            i += 1
    return {"diff_list": diff_list, "original_text": original_text, "processed_text": processed_text}

app.mount("/", StaticFiles(directory="static", html=True), name="static")