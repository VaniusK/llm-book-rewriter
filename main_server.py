from file_handler import FileHandler
from starlette.staticfiles import StaticFiles
import logging
import asyncio
from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Form
from fastapi.responses import FileResponse
import zipfile
import io
import os
from pathlib import Path
import json
from book_processor import BookProcessor
from config import load_config, deep_merge_dicts, config_local_filename
import difflib


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.getLogger('google_genai').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)

tasks: dict[str, (asyncio.Task, Path, Path)] = {}

app = FastAPI()

MAX_FILE_SIZE = 1024 * 1024 * 10
SUPPORTED_EXTENSIONS = ["fb2", "txt", "docx"]
OUTPUT_DIR = Path("output_books")
INPUT_DIR = Path("input_books")
INPUT_DIR.mkdir(parents=True, exist_ok=True)

def remove_file(path: Path):
    if os.path.exists(path):
        os.remove(path)

@app.post("/process/file")
async def process_file(config_str: str = Form(...), file: UploadFile = File(...)):
    config_tmp = json.loads(config_str)
    config = deep_merge_dicts(config_tmp, load_config(Path(config_local_filename)))
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Разрешены только файлы с расширением .zip")
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
        tasks[id] = (asyncio.create_task(book_processor.process_book(input_file, output_file)), input_file, output_file, original_filename, file.filename, config)
    return {"message": "Начата обработка файла", "task_id": id}

@app.get("/tasks/{task_id}")
async def check_task_status(task_id: str):
    if not task_id in tasks:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    return {"is_completed": tasks[task_id][0].done()}

@app.get("/tasks/{task_id}/result")
async def get_task_result(task_id: str, background_tasks: BackgroundTasks):
    if not task_id in tasks:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    if not tasks[task_id][0].done():
        raise HTTPException(status_code=400, detail="Задача ещё не завершена")

    with zipfile.ZipFile(task_id + ".zip", 'w') as z:
        z.write(OUTPUT_DIR / tasks[task_id][2], arcname=tasks[task_id][3])

    background_tasks.add_task(remove_file, task_id + ".zip")
    background_tasks.add_task(remove_file, tasks[task_id][1])
    background_tasks.add_task(remove_file, OUTPUT_DIR / tasks[task_id][2])
    background_tasks.add_task(lambda: tasks.pop(task_id))
    return FileResponse(
        path=task_id + ".zip",
        filename=tasks[task_id][4],
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
    matcher = difflib.SequenceMatcher(isjunk=None, a=original_text, b=processed_text, autojunk=True)

    diff_list = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            continue 
            
        diff_item = {
            "operation": tag,
            "source_range": (i1, i2),
            "target_range": (j1, j2),
            "text_removed": original_text[i1:i2],
            "text_added": processed_text[j1:j2]
        }
        diff_list.append(diff_item)
    return {"diff_list": diff_list, "original_text": original_text, "processed_text": processed_text}

app.mount("/", StaticFiles(directory="static", html=True), name="static")