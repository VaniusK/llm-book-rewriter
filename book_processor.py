import os
import re
import time
import logging
import asyncio
from typing import List
from config import config
from file_handler import FileHandler
from heuristic_applier import HeuristicApplier
from google import genai
from llm import LLM

class ValidationFailedError(Exception):
    pass

class ProcessingFailedError(Exception):
    pass

class BookProcessor:
    """
    A class for processing books by splitting them into chunks,
    processing each chunk with an LLM, and reassembling the processed chunks.
    """
    def __init__(self, llm_provider: str, file_type: str, result_filename: str):
        self.llm = LLM(llm_provider).llm
        os.makedirs(config["processing"]["output_dir"], exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.file_handler = FileHandler(file_type).file_handler
        self.heuristic_applier = HeuristicApplier()
        self.book_extension = file_type
        self.semaphore = asyncio.Semaphore(config["processing"]["workers_amount"])
        self.result_filename = result_filename

    def split_into_chunks(self, text: str, chunk_size: int) -> list[str]:
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
            processed_part = processed_parts[i]
            if re.fullmatch(tag_pattern, original_part):
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

    async def process_chunk(self, chunk: str, i: int, chunks: List[str], book_name: str) -> str:
        processed_chunk_text = chunk

        i2 = 0
        retries_available = config["processing"]["number_of_retries"]
        async with self.semaphore:
            while i2 < config["processing"]["number_of_passes"]:
                previous_processed_chunk = processed_chunk_text
                error_occurred = False
                if i2 == 0:
                    self.logger.info(
                        f"Processing chunk {i + 1}/{len(chunks)}, pass {i2 + 1}/{config['processing']['number_of_passes']}")
                try:
                    # TODO: Maybe include original text in the prompt? Requires testing
                    full_prompt = config['prompt']
                    preprocessed_chunk, heuristic_state = self.heuristic_applier.apply_preprocessing(processed_chunk_text, i2 == 0)
                    full_prompt = full_prompt.format(text_chunk=preprocessed_chunk)
                    processed_chunk_text = await self.llm.generate(full_prompt)
                    processed_chunk_text = self.heuristic_applier.apply_postprocessing(processed_chunk_text, heuristic_state)
                    processed_chunk_text = self.format_response(chunk, processed_chunk_text)

                    if not self.validate_response(chunk, processed_chunk_text):
                        raise ValidationFailedError(f"Couldn't validate the chunk")
                except ValidationFailedError as e:
                    self.logger.error(str(e) + f" {i + 1}/{len(chunks)}")
                    self.logger.debug(chunk)
                    self.logger.debug(processed_chunk_text)

                    error_occurred = True
                except genai.errors.APIError as e:
                    if e.status == "RESOURCE_EXHAUSTED":
                        self.logger.error(f"API limit exhausted while processing chunk {i + 1}/{len(chunks)}")
                        retries_available += 1
                        await asyncio.sleep(5)
                    else:
                        self.logger.error(f"API error happened while processing chunk {i + 1}/{len(chunks)}: {e}")
                    error_occurred = True
                except Exception as e:
                    # TODO: Change to specific exceptions: filter, api limit, etc
                    self.logger.error(f"Exception happened while processing chunk {i + 1}/{len(chunks)}: {e}")
                    error_occurred = True

                if error_occurred:
                    processed_chunk_text = previous_processed_chunk
                    if retries_available > 0:
                        self.logger.warning("Couldn't process the chunk, retrying")
                        retries_available -= 1
                        await asyncio.sleep(1)
                        continue
                    else:
                        self.logger.error(f"Couldn't process the chunk {i + 1}/{len(chunks)}, skipping")
                        raise ProcessingFailedError(f"Couldn't process the chunk")
                i2 += 1
                chunk = processed_chunk_text
            await self.file_handler.save_processed_chunk_to_file(book_name, i, processed_chunk_text)
            self.logger.info(f"Successfully processed and saved chunk {i + 1}/{len(chunks)}")
            return processed_chunk_text

    async def process_book(self, filepath: str):
        """Process book by modifying each chunk with LLM."""
        self.logger.info(f"Processing: {filepath}")
        book_name = filepath[:filepath.rfind(".")]
        await self.file_handler.create_cache_dir(book_name)
        output_filepath = os.path.join(config["processing"]["output_dir"], f"{self.result_filename}.{self.book_extension}")

        text = self.file_handler.extract_text(filepath)
        chunks = self.split_into_chunks(text, config["processing"]["chunk_size"])

        tasks = []
        chunks_to_process = []
        indices_to_process = []
        processed_chunks_results = [""] * len(chunks)
        for i in range(len(chunks)):
            chunk = await self.file_handler.load_processed_chunk_from_file(book_name, i)
            if chunk is None:
                chunks_to_process.append(chunks[i])
                indices_to_process.append(i)
            else:
                processed_chunks_results[i] = chunk

        for i, chunk_index in enumerate(indices_to_process):
            chunk = chunks_to_process[i]
            task = asyncio.create_task(self.process_chunk(chunk, chunk_index, chunks, book_name), name=f"Chunk-{chunk_index + 1}")
            tasks.append(task)

        self.logger.info(f"Starting processing for {len(tasks)} chunks using up to {self.semaphore._value} concurrent workers.")

        start_time_processing = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end_time_processing = time.time()
        self.logger.info(f"Finished processing {len(tasks)} chunks in {end_time_processing - start_time_processing:.2f} seconds.")

        successful_chunks = 0
        failed_chunks_indices = []
        for i, result in enumerate(results):
            original_index = indices_to_process[i]
            if isinstance(result, Exception):
                self.logger.error(f"Task for chunk {original_index + 1} failed: {result}")
                failed_chunks_indices.append(original_index + 1)
                processed_chunks_results[original_index] = chunks[original_index]
            else:
                processed_chunks_results[original_index] = result
                successful_chunks += 1

        if failed_chunks_indices:
            self.logger.warning(f"Failed to process chunks (original content used): {failed_chunks_indices}")

        final_text = "".join(processed_chunks_results)

        try:
            await asyncio.to_thread(self.file_handler.insert_text, filepath, final_text, output_filepath)
            self.logger.info(f"Successfully assembled and saved final result to {output_filepath}")

        except Exception as e:
            self.logger.error(f"Failed to save final file {output_filepath}: {e}", exc_info=True)
        await self.file_handler.clear_chunk_cache(book_name)