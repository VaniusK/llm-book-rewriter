import os
import re
import time
import logging
from config import config
from file_handler import FileHandler
from llm import LLM

class BookProcessor:
    """
    A class for processing books by splitting them into chunks,
    processing each chunk with an LLM, and reassembling the processed chunks.
    """
    def __init__(self, llm_provider: str, file_type: str):
        self.llm = LLM(llm_provider).llm
        os.makedirs(config["processing"]["output_dir"], exist_ok=True)
        self.logger = logging.getLogger(__name__)


        self.file_handler = FileHandler(file_type).file_handler
        self.book_extension = file_type

    def split_into_chunks(self, text, chunk_size: int) -> list[str]:
        """Split text into chunks of(roughly) given size, considering tag/sentence endings."""
        ending_symbols = [".", "!", "?"]
        if ">" in text:
            ending_symbols = [">"]
        chunks = []
        current_chunk = ""
        current_chunk_size = 0
        processed_size = 0

        for char in text:
            segment_size = 1
            current_chunk += char
            current_chunk_size += segment_size

            if current_chunk_size >= chunk_size and char in ending_symbols and len(text) - processed_size >= chunk_size // 10:
                chunks.append(current_chunk)
                current_chunk = ""
                processed_size += current_chunk_size
                current_chunk_size = 0

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def format_response(self, original_chunk: str, processed_chunk: str) -> str:
        """Ensure correct special symbol usage on chunk edges and between xml tags."""
        tag_pattern = r"(<[^>]+>)"
        original_parts = re.split(tag_pattern, original_chunk)
        processed_parts = re.split(tag_pattern, processed_chunk)

        if len(original_parts) != len(processed_parts):
            return processed_chunk

        result_parts = []
        for i, original_part in enumerate(original_parts):
            if i >= len(processed_parts):
                 continue

            processed_part = processed_parts[i]

            if (re.fullmatch(tag_pattern, original_part)) or not original_part:
                result_parts.append(processed_part)
            else:
                leading_whitespace_match = re.match(r'^(\s*)', original_part)
                leading_whitespace = leading_whitespace_match.group(1) if leading_whitespace_match else ""

                trailing_whitespace_match = re.search(r'(\s*)$', original_part)
                trailing_whitespace = trailing_whitespace_match.group(1) if trailing_whitespace_match else ""

                core_content = processed_part.strip()

                if core_content:
                    formatted_part = leading_whitespace + core_content + trailing_whitespace
                    result_parts.append(formatted_part)
                else:
                    result_parts.append(original_part)

        return "".join(result_parts)

    def validate_response(self, original_chunk: str, processed_chunk: str) -> bool:
        """Validate if the processed chunk maintains the same number of tags as the original chunk."""
        return original_chunk.count("<") == processed_chunk.count("<") and original_chunk.count(
            ">") == processed_chunk.count(">")

    def _heuristic_remove_commas(self, text: str):
        """Remove commas from the text."""
        return text.replace(",", "")
    def apply_heuristics(self, prompt: str):
        """Apply heuristics to the prompt based on the configuration."""
        for heuristic_name, enabled in config['heuristics'].items():
            if enabled:
                method_name = f"_heuristic_{heuristic_name}"
                heuristic_function = getattr(self, method_name, None)

                if heuristic_function and callable(heuristic_function):
                    prompt = heuristic_function(prompt)
                else:
                    self.logger.warning(f"Couldn't apply the {heuristic_name} heuristic")
        return prompt

    def process_book(self, filepath: str):
        """Process book by modifying each chunk with LLM."""
        self.logger.info(f"Processing: {filepath}")
        book_name = filepath[:filepath.rfind(".")]
        output_filepath = os.path.join(config["processing"]["output_dir"], f"{book_name}_rewritten.{self.book_extension}")

        segments = self.file_handler.extract_text(filepath)
        chunks = self.split_into_chunks(segments, config["processing"]["chunk_size"])

        processed_chunks = [self.file_handler.load_processed_chunks()]
        chunks_processed = self.file_handler.load_processed_chunks_count()
        i = chunks_processed + 1
        while i < len(chunks):
            chunk = chunks[i]
            start_time = time.time()
            self.logger.info(f"Processing chunk {i + 1}/{len(chunks)}...")
            processed_chunk_text = chunk

            try:
                full_prompt = config['prompt']
                full_prompt = full_prompt.format(text_chunk=self.apply_heuristics(chunk))
                processed_chunk_text = self.llm.generate(full_prompt)
                processed_chunk_text = self.format_response(chunk, processed_chunk_text)
                assert self.validate_response(chunk, processed_chunk_text)
            except Exception as e:
                self.logger.error(f"Error processing chunk: {e}")
                if config["processing"]["retry_if_failed"]:
                    self.logger.warning("Couldn't process the chunk, retrying")
                    continue
                else:
                    self.logger.warning("Couldn't process the chunk, skipping")

            processed_chunks.append(processed_chunk_text)
            self.file_handler.save_processed_chunks(processed_chunk_text)
            self.file_handler.save_processed_chunks_count(i)
            self.logger.info(f"Chunk processed in {time.time() - start_time} seconds")
            self.file_handler.insert_text(filepath, ''.join(processed_chunks), output_filepath)
            self.logger.info(f"Saved current progress to {output_filepath}")
            i += 1
        self.file_handler.clear_processed_chunks()
        self.file_handler.save_processed_chunks_count(-1)
        self.logger.info(f"Processed {filepath} in {len(chunks)} chunks")