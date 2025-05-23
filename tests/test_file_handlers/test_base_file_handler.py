import unittest
import pathlib
from typing import Dict, Any

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()


class TestBaseFileHandler(unittest.TestCase):
    """
    Base class for testing file handlers behaviour.
    """

    handler_class = None
    input_file_name = None
    output_file_name = None

    def setUp(self):
        """Set up test environment."""
        if not all([self.handler_class, self.input_file_name, self.output_file_name]):
            self.fail("Subclass must define handler_class, input_file_name, and output_file_name")

        self.input_path = SCRIPT_DIR / self.input_file_name
        self.output_path = SCRIPT_DIR / self.output_file_name

        if not self.input_path.exists():
            self.fail("Input file doesn't exist")

    def tearDown(self):
        """Clean up test environment."""
        if self.output_path.exists():
            self.output_path.unlink()

    def _run_extraction_insertion_test(self, config: Dict[Any, Any]):
        """Run test for extracting/inserting text."""
        file_handler = self.handler_class(config)
        original_text = file_handler.extract_text(self.input_path)
        file_handler.insert_text(self.input_path, original_text, self.output_path)
        self.assertTrue(self.output_path.exists())
        inserted_text = file_handler.extract_text(self.output_path)
        self.assertEqual(original_text, inserted_text)
