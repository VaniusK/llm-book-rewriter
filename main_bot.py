import logging
import tempfile
import asyncio
from uuid import uuid4
import zipfile
import io
import os
from pathlib import Path
import json
from book_processor import BookProcessor
from config import load_config, deep_merge_dicts, config_local_filename, config_default_filename
# pyrefly: ignore [missing-import]
import time
from fastapi import UploadFile

# pyrefly: ignore [missing-import]
from aiogram import Bot, Dispatcher, types, F
# pyrefly: ignore [missing-import]
from aiogram.types import FSInputFile, ErrorEvent

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
MAX_CONCURRENT_TASKS_PER_USER = 3
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

bot: Bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
dispatcher = Dispatcher()

@dispatcher.message(F.document)
async def process_file(message: types.Message):
    document = message.document
    temp_file = tempfile.SpooledTemporaryFile(max_size=MAX_FILE_SIZE)
    
    await bot.download(file=message.document.file_id, destination=temp_file)
    temp_file.seek(0)
    
    file = UploadFile(
        file=temp_file, 
        filename=message.document.file_name,
        headers={"content-type": message.document.mime_type}
    )

    config = deep_merge_dicts(load_config(Path(config_default_filename)), load_config(Path(config_local_filename)))
    user_id = message.from_user.id
    if not file.filename.endswith('.zip'):
        raise Exception("Разрешены только файлы с расширением .zip")
    if len([task_id for task_id in tasks if tasks[task_id][7] == user_id]) >= MAX_CONCURRENT_TASKS_PER_USER:
        raise Exception("Превышен лимит на количество одновременных задач от одного пользователя")
    if len(tasks) > MAX_CONCURRENT_TASKS:
        raise Exception("Сервер перегружен")
    zip_properties = await file.read()
    original_filename = None
    id = str(uuid4())
    with zipfile.ZipFile(io.BytesIO(zip_properties)) as z:
        if len(z.namelist()) != 1:
            raise Exception("Архив должен содержать только один файл")
        for info in z.infolist():
            if info.file_size > MAX_FILE_SIZE:
                raise Exception("Превышен максимальный размер файла")
            
            original_filename = Path(info.filename)
            ext = original_filename.suffix[1:]
            info.filename = id + "." + ext
            if ext not in SUPPORTED_EXTENSIONS:
                    raise Exception("Архив содержит запрещенный файл: {original_filename}"
                    )
            z.extract(info, path=INPUT_DIR)
        book_processor = BookProcessor(config, ext)
        input_file = INPUT_DIR / Path(id + "." + ext)
        output_file = Path(f"{id}_rewritten." + ext)
        tasks[id] = (asyncio.create_task(book_processor.process_book(input_file, output_file)), input_file, output_file, original_filename, Path(file.filename), config, time.time(), user_id)
    
    temp_message = await message.answer("Идёт обработка...", reply_to_message_id=message.message_id)
    
    await tasks[id][0]
    with zipfile.ZipFile(id + ".zip", 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.write(OUTPUT_DIR / tasks[id][2], arcname=tasks[id][3])

    os.rename(id + ".zip", tasks[id][4].stem + "_rewritten.zip")
    document = FSInputFile(tasks[id][4].stem + "_rewritten.zip")
    await temp_message.delete()
    await message.answer_document(document, reply_to_message_id=message.message_id)
    remove_file(id + ".zip")
    remove_file(tasks[id][1])
    remove_file(OUTPUT_DIR / tasks[id][2])
    tasks.pop(id)

@dispatcher.error()
async def global_error_handler(event: ErrorEvent):
    logger = logging.getLogger(__name__)
    logger.error(f"Произошла ошибка: {event.exception}")
    
    if event.update.message:
        await event.update.message.reply(f"Ошибка: {event.exception}. Попробуйте позже")


async def main():
    asyncio.create_task(cleanup_task())
    await dispatcher.start_polling(bot)

asyncio.run(main())