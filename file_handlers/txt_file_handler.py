import logging
from file_handlers.base_file_handler import BaseFileHandler
from pathlib import Path


class TXTFileHandler(BaseFileHandler):
    """Class for handling TXT files."""

    def insert_text(self, original_filepath: Path, processed_text: str, output_filepath: Path) -> None:
        """Replace the content of a txt file with the processed chunks."""
        output_filepath.write_text(processed_text, encoding='utf-8')

    def extract_text(self, filepath: Path) -> str:
        """Extract the content from a txt file."""
        try:
            return filepath.read_text(encoding='utf-8')
        except FileNotFoundError:
            logging.error(f"File not found at {filepath}")
            return ""
        except UnicodeDecodeError:
            logging.error(f"Unable to decode file at {filepath} with utf-8 encoding.")
            return ""
