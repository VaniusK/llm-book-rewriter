import os
from book_processor import BookProcessor

supported_extensions = ["fb2", "txt", "docx"]
sys_files = ["processed_chunks.txt", "processed_chunks_count.txt"]

if __name__ == "__main__":

    for filename in os.listdir("."):
        if filename in sys_files:
            continue
        extension = filename[filename.rfind(".") + 1:]
        if extension != "fb2":
            continue
        if extension in supported_extensions:
            book_processor = BookProcessor("google", extension)
            book_processor.process_book(filename)
