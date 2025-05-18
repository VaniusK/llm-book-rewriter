import logging
from file_handlers.base_file_handler import BaseFileHandler


class TXTFileHandler(BaseFileHandler):
    """Class for handling TXT files."""

    def insert_text(self, original_filepath: str, processed_chunks: list[str], output_filepath: str) -> None:
        """Replace the content of a txt file with the processed chunks."""
        with open(output_filepath, 'w', encoding='utf-8') as output_file:
            output_file.write("".join(processed_chunks))

    def extract_text(self, filepath: str) -> str:
        """Extract the content from a txt file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            logging.error(f"File not found at {filepath}")
            return ""
        except UnicodeDecodeError:
            logging.error(f"Unable to decode file at {filepath} with utf-8 encoding.")
            return ""
