import unittest
from unittest.mock import patch
from unittest.mock import AsyncMock
from book_processor import BookProcessor
import book_processor
from pathlib import Path

config = {
    "processing": {
        "output_dir": "test_output",
        "chunk_size": 8000,
        "workers_amount": 3,
        "number_of_retries": 3,
        "number_of_passes": 1
    },
    "prompt": "{text_chunk}",
    "heuristics": {
        "remove_commas": False,
        "replace_tags_with_placeholder": True,
        "placeholder": "<image/>",
        "remove_thinking": False
    }
}


class TestBookProcessor(unittest.IsolatedAsyncioTestCase):
    """
    A class for testing BookProcessor behaviour.
    """

    output_file = Path("result.fb2")
    test_file = Path("test.fb2")

    @patch("book_processor.FileHandler")
    @patch("book_processor.LLM")
    def test_split_into_chunks(self, MockLLM, MockFileHandler):
        """Test split_into_chunks method."""
        processor = BookProcessor(config, "fb2")
        self.assertEqual(processor.split_into_chunks("0123456789>", 10), ["0123456789>"])
        self.assertEqual(processor.split_into_chunks("0123456789", 10), ["0123456789"])
        self.assertEqual(processor.split_into_chunks("0123456789>0123456789>", 10), ["0123456789>", "0123456789>"])
        self.assertEqual(processor.split_into_chunks("0123456789.0123456789", 10), ["0123456789.", "0123456789"])
        self.assertEqual(processor.split_into_chunks("0123456789!0123456789", 10), ["0123456789!", "0123456789"])

    @patch("book_processor.FileHandler")
    @patch("book_processor.LLM")
    def test_validate_response(self, MockLLM, MockFileHandler):
        """Test validate_response method."""
        processor = BookProcessor(config, "fb2")
        self.assertEqual(processor.validate_response("<p>Hi<p/>", "<p>Hi<p/>"), True)
        self.assertEqual(processor.validate_response("<p>Hi<p/>", "<p>Hi<p/"), False)
        self.assertEqual(processor.validate_response("<p>Hi<p/>", "<p>Hi"), False)

    @patch("book_processor.FileHandler")
    @patch("book_processor.LLM")
    def test_format_response(self, MockLLM, MockFileHandler):
        """Test format_response method."""
        processor = BookProcessor(config, "fb2")
        self.assertEqual(processor.format_response("<p> Let's go for a dog\t   <p/>", "<p>Let's go for a walk<p/>"),
                         "<p> Let's go for a walk\t   <p/>")
        self.assertEqual(processor.format_response("\n\nSome text\n\n", "\t New text \t"), "\n\nNew text\n\n")
        self.assertEqual(processor.format_response("<body> content <body/>", "\n  <body> content2 <body/>  \n"),
                         "<body> content2 <body/>")
        self.assertEqual(processor.format_response("<v>Как взор его был быстр и нежин,</v>", "<v> Как взор его был быстр и нежен, </v>"),
                         "<v>Как взор его был быстр и нежен,</v>")

    @patch("book_processor.FileHandler")
    @patch("book_processor.LLM")
    async def test_process_chunk(self, MockLLM, MockFileHandler):
        """Test process_chunk method."""

        async def return_same_text(text: str) -> str:
            return text

        async def return_modified_text(text: str) -> str:
            return text + "ahaha"

        async def return_random_text(text: str) -> str:
            return "m,nbhgvyyuijkm,nbhgyuhjkm"

        processor = BookProcessor(config, "fb2")
        mock_llm_instance = MockLLM.return_value.llm
        mock_file_handler_instance = MockFileHandler.return_value.file_handler
        processor.llm = mock_llm_instance
        processor.file_handler = mock_file_handler_instance
        mock_file_handler_instance.save_processed_chunk_to_file = AsyncMock()
        original_chunk = "<p> content </p>"
        mock_llm_instance.generate = AsyncMock(side_effect=return_same_text)
        processed_chunk = await processor.process_chunk(original_chunk, 0, 1, "test_book")
        self.assertEqual(processed_chunk, "<p> content </p>")
        self.assertEqual(mock_llm_instance.generate.call_count, 1)
        self.assertEqual(mock_file_handler_instance.save_processed_chunk_to_file.call_count, 1)

        mock_llm_instance.generate = AsyncMock(side_effect=return_modified_text)
        processed_chunk = await processor.process_chunk(original_chunk, 0, 1, "test_book")
        self.assertEqual(processed_chunk, "<p> content </p>ahaha")
        self.assertEqual(mock_llm_instance.generate.call_count, 1)
        self.assertEqual(mock_file_handler_instance.save_processed_chunk_to_file.call_count, 2)

        mock_llm_instance.generate = AsyncMock(side_effect=return_random_text)
        with self.assertRaises(book_processor.ProcessingFailedError):
            await processor.process_chunk(original_chunk, 0, 1, "test_book")
        self.assertEqual(mock_llm_instance.generate.call_count, 3)
        self.assertEqual(mock_file_handler_instance.save_processed_chunk_to_file.call_count, 2)

    @patch("book_processor.LLM")
    async def test_process_book(self, MockLLM):
        """Test process_book method."""

        async def return_same_text(text: str) -> str:
            return text

        processor = BookProcessor(config, "fb2")
        mock_llm_instance = MockLLM.return_value.llm
        processor.llm = mock_llm_instance
        mock_llm_instance.generate = AsyncMock(side_effect=return_same_text)
        await processor.process_book(self.test_file, self.output_file)
        processed_file_path = Path(config["processing"]["output_dir"]) / self.output_file
        self.assertTrue(processed_file_path.exists())
        original_text = processor.file_handler.extract_text(self.test_file)
        processed_text = processor.file_handler.extract_text(processed_file_path)
        self.assertEqual(original_text, processed_text)
        processed_file_path.unlink()


if __name__ == '__main__':
    unittest.main()
