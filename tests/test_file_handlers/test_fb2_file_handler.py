import unittest
from file_handlers.fb2_file_handler import FB2FileHandler
from tests.test_file_handlers.test_base_file_handler import TestBaseFileHandler
import pathlib

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()

class TestFB2FileHandler(TestBaseFileHandler):
    """
    A class for testing FB2 file handlers behaviour.
    """
    def setUp(self):
        """Set up test environment."""
        self.handler_class = FB2FileHandler
        self.input_file_name = "test.fb2"
        self.output_file_name = "result.fb2"
        super().setUp()

    def test_extract_insert_text(self):
        """Run test for extracting/inserting text."""
        config = dict()
        self._run_extraction_insertion_test(config)

if __name__ == '__main__':
    unittest.main()
