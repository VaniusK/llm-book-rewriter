import unittest
from heuristic_applier import HeuristicApplier

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


class TestHeuristicApplier(unittest.TestCase):
    """
    A class for testing HeuristicApplier behaviour.
    """

    def test_heuristics(self):
        """Test heuristics."""
        heuristic_applier = HeuristicApplier(config)
        self.assertEqual(heuristic_applier.preprocessing_remove_commas("Apples, bananas, oranges"),
                         ["Apples bananas oranges", {}])
        self.assertEqual(heuristic_applier.preprocessing_replace_tags_with_placeholder("<br> text <br>"),
                         [" <image/>  text  <image/> ", {"replaced_tags": ["<br>", "<br>"]}])
        self.assertEqual(heuristic_applier.postprocessing_replace_tags_with_placeholder("<image/> text <image/>", {
            "replaced_tags": ["<br>", "<br>"]}), "<br> text <br>")


if __name__ == '__main__':
    unittest.main()
