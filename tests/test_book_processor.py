import unittest
from unittest.mock import patch
from book_processor import BookProcessor
from config import config
from heuristic_applier import HeuristicApplier

@patch.dict(config, {'processing': {'output_dir': 'test_output'}}, clear=True)
@patch('book_processor.FileHandler')
@patch('book_processor.LLM')
class TestBookProcessor(unittest.TestCase):
    def test_split_into_chunks(self, MockLLM, MockFileHandler):
        processor = BookProcessor("google", "fb2")
        self.assertEqual(processor.split_into_chunks("0123456789>", 10), ["0123456789>"])
        self.assertEqual(processor.split_into_chunks("0123456789", 10), ["0123456789"])
        self.assertEqual(processor.split_into_chunks("0123456789>0123456789>", 10), ["0123456789>", "0123456789>"])
        self.assertEqual(processor.split_into_chunks("0123456789.0123456789", 10), ["0123456789.", "0123456789"])
        self.assertEqual(processor.split_into_chunks("0123456789!0123456789", 10), ["0123456789!", "0123456789"])

    def test_validate_response(self, MockLLM, MockFileHandler):
        processor = BookProcessor("google", "fb2")
        self.assertEqual(processor.validate_response("<p>Hi<p/>", "<p>Hi<p/>"), True)
        self.assertEqual(processor.validate_response("<p>Hi<p/>", "<p>Hi<p/"), False)
        self.assertEqual(processor.validate_response("<p>Hi<p/>", "<p>Hi"), False)

    def test_format_response(self, MockLLM, MockFileHandler):
        processor = BookProcessor("google", "fb2")
        self.assertEqual(processor.format_response("<p> Let's go for a dog\t   <p/>", "<p>Let's go for a walk<p/>"),"<p> Let's go for a walk\t   <p/>")
        self.assertEqual(processor.format_response("\n\nSome text\n\n", "\t New text \t"),"\n\nNew text\n\n")

    def test_heuristics(self, MockLLM, MockFileHandler):
        heuristic_applier = HeuristicApplier()
        self.assertEqual(heuristic_applier.preprocessing_remove_commas("Apples, bananas, oranges"), ["Apples bananas oranges", {}])
        self.assertEqual(heuristic_applier.preprocessing_replace_tags_with_placeholder("<br> text <br>"), ["@ text @", {"replaced_tags": ["br", "br"], "placeholder": "@"}])
        self.assertEqual(heuristic_applier.postprocessing_replace_tags_with_placeholder("@ text @", {"replaced_tags": ["br", "br"], "placeholder": "@"}), "<br> text <br>")
        self.assertEqual(heuristic_applier.preprocessing_replace_tags_with_placeholder("<br> text@ <br>"), ["# text@ #", {"replaced_tags": ["br", "br"], "placeholder": "#"}])
        self.assertEqual(heuristic_applier.postprocessing_replace_tags_with_placeholder("# text@ #", {"replaced_tags": ["br", "br"], "placeholder": "#"}), "<br> text@ <br>")


if __name__ == '__main__':
    unittest.main()
