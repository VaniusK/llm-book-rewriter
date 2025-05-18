import unittest
from file_handlers.txt_file_handler import TXTFileHandler
from tests.test_file_handlers.test_base_file_handler import TestBaseFileHandler
import pathlib

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()

class TestTXTileHandler(TestBaseFileHandler):
    """
    A class for testing TXT file handlers behaviour.
    """
    def setUp(self):
        """Set up test environment."""
        self.handler_class = TXTFileHandler
        self.input_file_name = "test.txt"
        self.output_file_name = "result.txt"
        super().setUp()

    def test_extract_insert_text(self):
        """Run test for extracting/inserting."""
        config = dict()
        self._run_extraction_insertion_test(config)

if __name__ == '__main__':
    unittest.main()
