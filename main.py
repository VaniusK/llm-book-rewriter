import logging
import asyncio
from config import config
from pathlib import Path
from book_processor import BookProcessor


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.getLogger('google_genai').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)

supported_extensions = ["fb2", "txt", "docx"]
sys_files = ["requirements.txt"]

logger = logging.getLogger(__name__)
input_directory = Path(".")

if __name__ == "__main__":

    for file in input_directory.iterdir():
        filename = file.stem
        extension = file.suffix[1:]
        if file in sys_files:
            continue
        if extension in supported_extensions:
            book_processor = BookProcessor(config, extension)
            asyncio.get_event_loop().run_until_complete(book_processor.process_book(file, Path(f"{filename}_rewritten." + extension)))
