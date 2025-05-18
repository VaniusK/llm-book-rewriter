import unittest
from file_handlers.docx_file_handler import DOCXFileHandler
from tests.test_file_handlers.test_base_file_handler import TestBaseFileHandler


class TestDOCXFileHandler(TestBaseFileHandler):
    """
    A class for testing DOCX file handlers behaviour.
    """
    def setUp(self):
        """Set up test environment."""
        self.handler_class = DOCXFileHandler
        self.input_file_name = "test.docx"
        self.output_file_name = "result.docx"
        super().setUp()

    def test_extract_insert_text_with_merging(self):
        """Run test for extracting/inserting text with tag merging."""
        config = {
            "processing": {
                "docx_merge_runs": True
            }
        }
        self._run_extraction_insertion_test(config)

    def test_extract_insert_text_without_merging(self):
        """Run test for extracting/inserting text without tag merging."""
        config = {
            "processing": {
                "docx_merge_runs": False
            }
        }
        self._run_extraction_insertion_test(config)

if __name__ == '__main__':
    unittest.main()
