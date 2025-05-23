import shutil
from abc import ABC, abstractmethod
from pathlib import Path
import asyncio


class BaseFileHandler(ABC):
    """
    Abstract interface for all file handlers.
    Provides common methods for async caching.
    """

    book_temp_dir = "book_temp"

    def __init__(self, config: dict[any, any]):
        """Initialize the FileHandler."""
        self.config = config

    @abstractmethod
    def insert_text(self, original_filepath: Path, processed_text: str, output_filepath: Path):
        """Insert processed text chunks into a file."""
        pass

    @abstractmethod
    def extract_text(self, filepath: Path):
        """Extract text from a file."""
        pass

    async def _get_cache_dir(self, book_name: str) -> Path:
        """Get cache directory of the book."""
        cache_dir = Path(self.book_temp_dir) / book_name
        return cache_dir

    async def _get_chunk_filepath(self, book_name: str, chunk_index: int) -> Path:
        """Get filepath of the given chunk of the book."""
        book_dir = await self._get_cache_dir(book_name)
        return book_dir / Path(f"chunk{chunk_index:05d}.txt")

    async def create_cache_dir(self, book_name: Path):
        """Create cache directory of the book."""
        cache_dir = Path(self.book_temp_dir) / book_name
        await asyncio.to_thread(cache_dir.mkdir, parents=True, exist_ok=True)

    async def save_processed_chunk_to_file(self, book_name: str, chunk_index: int, chunk_text: str):
        """Save processed chunk to a file."""
        chunk_filepath = await self._get_chunk_filepath(book_name, chunk_index)
        await asyncio.to_thread(chunk_filepath.write_text, chunk_text, encoding="utf-8")

    async def load_processed_chunk_from_file(self, book_name: str, chunk_index: int) -> str | None:
        """Load processed chunk from a file."""
        chunk_filepath = await self._get_chunk_filepath(book_name, chunk_index)
        if await asyncio.to_thread(chunk_filepath.exists):
            return await asyncio.to_thread(chunk_filepath.read_text, encoding="utf-8")
        return None

    async def clear_chunk_cache(self, book_name: str):
        """Clear chunk cache by deleting book's cache directory."""
        book_dir = await self._get_cache_dir(book_name)
        return await asyncio.to_thread(
            lambda: shutil.rmtree(book_dir)
        )
