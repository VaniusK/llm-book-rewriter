from typing import List
import re
from file_handlers.base_file_handler import BaseFileHandler

class FB2FileHandler(BaseFileHandler):
    def insert_text(self, original_filepath: str, processed_chunks: List[str], output_filepath: str):
        """Replace fb2's <body> with given text."""
        with open(original_filepath, 'r', encoding="utf-8") as input_file:
            with open(output_filepath, 'w', encoding="utf-8") as output_file:
                input_file_text = input_file.read()
                pattern = r"<body.*?>(.*?)</body>"
                flags = re.DOTALL | re.IGNORECASE
                input_file_text = re.sub(pattern, f"{processed_chunks}", input_file_text, flags=flags)
                output_file.write(input_file_text)

    def extract_text(self, filepath: str) -> str:
        """Extract fb2's <body> content."""
        with open(filepath, 'r', encoding="utf-8") as f:
            content = f.read()
            pattern = r"<body.*?>.*?</body>"
            flags = re.DOTALL | re.IGNORECASE
            match = re.search(pattern, content, flags=flags)
            if match:
                return match.group(0)
            else:
                return ""
