from abc import ABC, abstractmethod
from typing import List
import os

class BaseFileHandler(ABC):
    def __init__(self, processed_chunks_file="processed_chunks.txt",
                 processed_chunks_count_file="processed_chunks_count.txt"):
        self.processed_chunks_file: str = processed_chunks_file
        self.processed_chunks_count_file: str = processed_chunks_count_file

    @abstractmethod
    def insert_text(self, original_filepath: str, processed_chunks: List[str], output_filepath: str):
        pass

    @abstractmethod
    def extract_text(self, filepath: str):
        pass

    def save_processed_chunks(self, chunk: str):
        with open(self.processed_chunks_file, "a", encoding="utf-8") as file:
            file.write(chunk)

    def clear_processed_chunks(self):
        with open(self.processed_chunks_file, "w", encoding="utf-8") as file:
            file.write("")

    def load_processed_chunks(self):
        if not os.path.exists(self.processed_chunks_file):
            return ""
        with open(self.processed_chunks_file, "r", encoding="utf-8") as file:
            return file.read()

    def save_processed_chunks_count(self, chunk_count: int):
        with open(self.processed_chunks_count_file, "w", encoding="utf-8") as file:
            file.write(str(chunk_count))

    def load_processed_chunks_count(self):
        if not os.path.exists(self.processed_chunks_count_file):
            return 0
        with open(self.processed_chunks_count_file, "r", encoding="utf-8") as file:
            f = file.read()
            return int(f) if f else -1