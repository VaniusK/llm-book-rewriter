import re
import time
import logging
from pathlib import Path
import asyncio
from tqdm.asyncio import tqdm
from file_handler import FileHandler
from heuristic_applier import HeuristicApplier
from llm import LLM


class ValidationFailedError(Exception):
    """Raised when LLM response validation fails (e.g., tag mismatch)."""
    pass

class ProcessingFailedError(Exception):
    """Raised when the code fails to process chunk in configured number of tries."""
    pass


async def tqdm_gather(*fs, return_exceptions=False, **kwargs):
    """
    tqdm wrapper because asyncio.gather doesn't support return_exceptions param for some reason.
    So here is a workaround.
    """
    if not return_exceptions:
        return await tqdm.gather(*fs, **kwargs)

    async def wrap(f):
        try:
            return await f
        except Exception as e:
            return e

    return await tqdm.gather(*map(wrap, fs), **kwargs)

class BookProcessor:
    """
    A class for processing books by splitting them into chunks,
    processing each chunk with an LLM, and reassembling the processed chunks.
    """
    def __init__(self, config: dict[any, any], file_type: str):
        """
            Initializes the BookProcessor.

            Args:
                file_type: The extension of the book file (e.g., 'fb2', 'txt').
                config: Configuration dictionary containing settings for
                                         processing, LLM, file handling, etc.
            """
        self.config = config
        self.llm = LLM(self.config).llm
        self.output_dir = Path(config["processing"]["output_dir"])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.file_handler = FileHandler(file_type, self.config).file_handler
        self.heuristic_applier = HeuristicApplier(self.config)
        self.book_extension = file_type
        self.semaphore = asyncio.Semaphore(self.config["processing"]["workers_amount"])

    def split_into_chunks(self, text: str, chunk_size: int) -> list[str]:
        """
        Split text into chunks of(roughly) given size, considering tag/sentence endings.
        Avoids creating overly small final chunks.

        Args:
            text: The input text to split.
            chunk_size: The desired approximate size for each chunk.

        Returns:
            A list of text chunks.
        """
        ending_symbols = [".", "!", "?", "\n"]
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
        """
        Formats the processed chunk to preserve original whitespace and tag structure.

        It ensures that leading/trailing whitespace around non-tag content in the
        original chunk is maintained in the processed chunk, and that tags
        themselves are preserved.

        Args:
            original_chunk: The original text chunk before LLM processing.
            processed_chunk: The text chunk after LLM processing.

        Returns:
            The formatted processed chunk.
        """
        tag_pattern = r"(<.*?>)"
        original_parts = re.split(tag_pattern, original_chunk)
        processed_parts = re.split(tag_pattern, processed_chunk)

        if len(original_parts) != len(processed_parts):
            return processed_chunk

        result_parts = []
        for i, original_part in enumerate(original_parts):
            processed_part = processed_parts[i]
            if re.fullmatch(tag_pattern, original_part):
                result_parts.append(original_part)
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

    async def process_chunk(self, chunk: str, i: int, total_chunks: int, book_name: str) -> str:
        """
        Processes a single text chunk using the LLM with multiple passes and retries.

        The processing involves:
        1. Applying pre-processing heuristics.
        2. Sending the chunk to the LLM (multiple passes if configured).
        3. Applying post-processing heuristics.
        4. Formatting the response to preserve original structure.
        5. Validating the processed chunk (e.g., tag count).
        Handles API errors and validation failures with retries.
        Uses a semaphore to limit concurrent LLM calls. Saves the processed
        chunk to a cache file.

        Args:
            chunk: The text chunk to process.
            i: The index of the current chunk in the list of all chunks.
            total_chunks: Total amount of chunks in the book, used for logging.
            book_name: The name of the book, used for caching.

        Returns:
            The processed text chunk.

        Raises:
            ProcessingFailedError: If the chunk cannot be processed successfully
                                   after all retries.
        """
        processed_chunk_text = chunk

        i2 = 0
        retries_available = self.config["processing"]["number_of_retries"] - 1
        async with self.semaphore:
            while i2 < self.config["processing"]["number_of_passes"]:
                previous_processed_chunk = processed_chunk_text
                error_occurred = False
                if i2 == 0:
                    self.logger.info(
                        f"Processing chunk {i + 1}/{total_chunks}, pass {i2 + 1}/{self.config['processing']['number_of_passes']}")
                try:
                    # TODO: Maybe include original text in the prompt? Requires testing
                    full_prompt = self.config['prompt']
                    preprocessed_chunk, heuristic_state = self.heuristic_applier.apply_preprocessing(processed_chunk_text, i2 == 0)
                    full_prompt = full_prompt.format(text_chunk=preprocessed_chunk)
                    processed_chunk_text = await self.llm.generate(full_prompt)
                    processed_chunk_text = self.heuristic_applier.apply_postprocessing(processed_chunk_text, heuristic_state)
                    processed_chunk_text = self.format_response(chunk, processed_chunk_text)

                    if not self.validate_response(chunk, processed_chunk_text):
                        raise ValidationFailedError(f"Couldn't validate the chunk")
                except ValidationFailedError as e:
                    self.logger.error(str(e) + f" {i + 1}/{total_chunks}")
                    self.logger.debug(chunk)
                    self.logger.debug(processed_chunk_text)

                    error_occurred = True
                except Exception as e:
                    # TODO: Change to specific exceptions: filter, api limit, etc
                    self.logger.error(f"Exception happened while processing chunk {i + 1}/{total_chunks}: {e}")
                    error_occurred = True

                if error_occurred:
                    processed_chunk_text = previous_processed_chunk
                    if retries_available > 0:
                        self.logger.warning("Couldn't process the chunk, retrying")
                        retries_available -= 1
                        await asyncio.sleep(1)
                        continue
                    else:
                        self.logger.error(f"Couldn't process the chunk {i + 1}/{total_chunks}, skipping")
                        raise ProcessingFailedError(f"Couldn't process the chunk")
                i2 += 1
                chunk = processed_chunk_text
            await self.file_handler.save_processed_chunk_to_file(book_name, i, processed_chunk_text)
            self.logger.info(f"Successfully processed and saved chunk {i + 1}/{total_chunks}")
            return processed_chunk_text

    async def process_book(self, input_file: Path, output_file: Path):
        """
        Processes an entire book file.

        The process includes:
        1. Extracting text from the file.
        2. Splitting the text into manageable chunks.
        3. Checking a cache for already processed chunks.
        4. Asynchronously processing any new or unprocessed chunks using `process_chunk`.
        5. Reassembling the processed chunks into the final text.
        6. Saving the final text to a new file.
        7. Clearing the chunk cache for the book.

        Args:
            input_file: The book to be processed.
            output_file: Name of the processed book's file.
    """
        self.logger.info(f"Processing: {input_file}")
        book_name = input_file.stem
        await self.file_handler.create_cache_dir(book_name)
        output_filepath = Path(self.config["processing"]["output_dir"]) / output_file

        text = self.file_handler.extract_text(input_file)
        chunks = self.split_into_chunks(text, self.config["processing"]["chunk_size"])

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
            task = asyncio.create_task(self.process_chunk(chunk, chunk_index, len(chunks), book_name), name=f"Chunk-{chunk_index + 1}")
            tasks.append(task)

        self.logger.info(f"Starting processing for {len(tasks)} chunks using up to {self.semaphore._value} concurrent workers.")

        start_time_processing = time.time()
        results = await tqdm_gather(*tasks, desc=f"Processing {input_file}", total=len(chunks), initial=len(chunks) - len(indices_to_process), bar_format="{l_bar}{bar}{r_bar}\n", return_exceptions=True)
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
            await asyncio.to_thread(self.file_handler.insert_text, input_file, final_text, output_filepath)
            self.logger.info(f"Successfully assembled and saved final result to {output_filepath}")

        except Exception as e:
            self.logger.error(f"Failed to save final file {output_filepath}: {e}", exc_info=True)
        await self.file_handler.clear_chunk_cache(book_name)