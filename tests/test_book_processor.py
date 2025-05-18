import unittest
from unittest.mock import patch
from unittest.mock import AsyncMock
import os
from heuristic_applier import HeuristicApplier
from book_processor import BookProcessor
import book_processor


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
        "placeholder": "<image/>"
    }
}
class TestBookProcessor(unittest.IsolatedAsyncioTestCase):

    @patch("book_processor.FileHandler")
    @patch("book_processor.LLM")
    def test_split_into_chunks(self, MockLLM, MockFileHandler):
        processor = BookProcessor("fb2", "result.fb2", config)
        self.assertEqual(processor.split_into_chunks("0123456789>", 10), ["0123456789>"])
        self.assertEqual(processor.split_into_chunks("0123456789", 10), ["0123456789"])
        self.assertEqual(processor.split_into_chunks("0123456789>0123456789>", 10), ["0123456789>", "0123456789>"])
        self.assertEqual(processor.split_into_chunks("0123456789.0123456789", 10), ["0123456789.", "0123456789"])
        self.assertEqual(processor.split_into_chunks("0123456789!0123456789", 10), ["0123456789!", "0123456789"])

    @patch("book_processor.FileHandler")
    @patch("book_processor.LLM")
    def test_validate_response(self, MockLLM, MockFileHandler):
        processor = BookProcessor("fb2", "result.fb2", config)
        self.assertEqual(processor.validate_response("<p>Hi<p/>", "<p>Hi<p/>"), True)
        self.assertEqual(processor.validate_response("<p>Hi<p/>", "<p>Hi<p/"), False)
        self.assertEqual(processor.validate_response("<p>Hi<p/>", "<p>Hi"), False)

    @patch("book_processor.FileHandler")
    @patch("book_processor.LLM")
    def test_format_response(self, MockLLM, MockFileHandler):
        processor = BookProcessor("fb2", "result.fb2", config)
        self.assertEqual(processor.format_response("<p> Let's go for a dog\t   <p/>", "<p>Let's go for a walk<p/>"),"<p> Let's go for a walk\t   <p/>")
        self.assertEqual(processor.format_response("\n\nSome text\n\n", "\t New text \t"),"\n\nNew text\n\n")
        self.assertEqual(processor.format_response("<body> content <body/>", "\n  <body> content2 <body/>  \n"),"<body> content2 <body/>")

    @patch("book_processor.FileHandler")
    @patch("book_processor.LLM")
    async def test_process_chunk(self, MockLLM, MockFileHandler):
        async def return_same_text(text: str) -> str:
            return text

        async def return_modified_text(text: str) -> str:
            return text + "ahaha"

        async def return_random_text(text: str) -> str:
            return "m,nbhgvyyuijkm,nbhgyuhjkm"

        processor = BookProcessor("fb2", "result", config)
        mock_llm_instance = MockLLM.return_value.llm
        mock_file_handler_instance = MockFileHandler.return_value.file_handler
        processor.llm = mock_llm_instance
        processor.file_handler = mock_file_handler_instance
        mock_file_handler_instance.save_processed_chunk_to_file = AsyncMock()
        original_chunk = "<p> content </p>"
        mock_llm_instance.generate = AsyncMock(side_effect=return_same_text)
        processed_chunk = await processor.process_chunk(original_chunk, 0, [original_chunk], "test_book")
        self.assertEqual(processed_chunk, "<p> content </p>")
        self.assertEqual(mock_llm_instance.generate.call_count, 1)
        self.assertEqual(mock_file_handler_instance.save_processed_chunk_to_file.call_count, 1)

        mock_llm_instance.generate = AsyncMock(side_effect=return_modified_text)
        processed_chunk = await processor.process_chunk(original_chunk, 0, [original_chunk], "test_book")
        self.assertEqual(processed_chunk, "<p> content </p>ahaha")
        self.assertEqual(mock_llm_instance.generate.call_count, 1)
        self.assertEqual(mock_file_handler_instance.save_processed_chunk_to_file.call_count, 2)

        mock_llm_instance.generate = AsyncMock(side_effect=return_random_text)
        with self.assertRaises(book_processor.ProcessingFailedError):
            await processor.process_chunk(original_chunk, 0, [original_chunk], "test_book")
        self.assertEqual(mock_llm_instance.generate.call_count, 3)
        self.assertEqual(mock_file_handler_instance.save_processed_chunk_to_file.call_count, 2)

    @patch("book_processor.LLM")
    async def test_process_book(self, MockLLM):
        async def return_same_text(text: str) -> str:
            return text

        processor = BookProcessor("fb2", "result", config)
        mock_llm_instance = MockLLM.return_value.llm
        processor.llm = mock_llm_instance
        original_chunk = "<p> content </p>"
        mock_llm_instance.generate = AsyncMock(side_effect=return_same_text)
        await processor.process_book("test.fb2")
        processed_file_path = os.path.join(config["processing"]["output_dir"], "result.fb2")
        self.assertTrue(os.path.exists(processed_file_path))
        original_text = processor.file_handler.extract_text("test.fb2")
        processed_text = processor.file_handler.extract_text(processed_file_path)
        self.assertEqual(original_text, processed_text)
        os.remove(processed_file_path)


    def test_heuristics(self):
        heuristic_applier = HeuristicApplier(config)
        self.assertEqual(heuristic_applier.preprocessing_remove_commas("Apples, bananas, oranges"), ["Apples bananas oranges", {}])
        self.assertEqual(heuristic_applier.preprocessing_replace_tags_with_placeholder("<br> text <br>"), [" <image/>  text  <image/> ", {"replaced_tags": ["<br>", "<br>"], "placeholder": "<image/>"}])
        self.assertEqual(heuristic_applier.postprocessing_replace_tags_with_placeholder("<image/> text <image/>", {"replaced_tags": ["<br>", "<br>"], "placeholder": "<image/>"}), "<br> text <br>")


if __name__ == '__main__':
    unittest.main()
