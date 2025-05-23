import re
from file_handlers.base_file_handler import BaseFileHandler
from pathlib import Path


class FB2FileHandler(BaseFileHandler):
    """Class for handling FB2 files."""

    def insert_text(self, original_filepath: Path, processed_text: str, output_filepath: Path):
        """Replace fb2's <body> with given text."""
        input_file_text = original_filepath.read_text(encoding = "utf-8")
        pattern = r"<body.*?>(.*?)</body>"
        flags = re.DOTALL | re.IGNORECASE
        resulting_text = re.sub(pattern, f"{processed_text}", input_file_text, flags=flags)
        output_filepath.write_text(resulting_text, encoding = "utf-8")

    def extract_text(self, filepath: Path) -> str:
        """Extract fb2's <body> content."""
        content = filepath.read_text(encoding = "utf-8")
        pattern = r"<body.*?>.*?</body>"
        flags = re.DOTALL | re.IGNORECASE
        match = re.search(pattern, content, flags=flags)
        if match:
            return match.group(0)
        else:
            return ""
