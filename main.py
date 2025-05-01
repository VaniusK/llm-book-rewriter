import logging
from config import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.getLogger('google_genai').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
import os
from book_processor import BookProcessor

supported_extensions = ["fb2", "txt", "docx"]
sys_files = ["processed_chunks.txt", "processed_chunks_count.txt", "requirements.txt"]

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    for filename in os.listdir("."):
        if filename in sys_files:
            continue
        extension = filename[filename.rfind(".") + 1:]
        if extension != "fb2":
            continue
        if extension in supported_extensions:
            book_processor = BookProcessor(config["processing"]["provider"], extension)
            book_processor.process_book(filename)
