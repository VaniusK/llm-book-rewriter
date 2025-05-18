import re
import logging

class HeuristicApplier:
    """
    A class for applying preprocessing and postprocessing heuristic to text prompt.

    self.preprocessing_original_heuristics would only run on chunk's first pass.
    """

    def __init__(self, config: dict[any, any]):
        """
        Initializes HeuristicApplied based on config
        uses
            preprocessing_{heuristic}
        and
            postprocessing_{heuristic}
        naming convention
        """
        self.logger = logging.getLogger(__name__)
        self.preprocessing_original_heuristics = [self.preprocessing_remove_commas]
        self.preprocessing_heuristics = [self.preprocessing_replace_tags_with_placeholder]
        self.postprocessing_heuristics = [self.postprocessing_replace_tags_with_placeholder]
        self.placeholder = config["heuristics"]["placeholder"]
        self.config = config

    def apply_preprocessing(self, prompt: str, is_original: bool) -> list[any]:
        """Apply preprocessing heuristics to the prompt based on the configuration."""
        postprocessing_info = dict()
        if is_original:
            for heuristic in self.preprocessing_original_heuristics:
                if self.config ['heuristics'][heuristic.__name__[(heuristic.__name__).find("_") + 1:]]:
                    result = heuristic(prompt)
                    prompt = result[0]
                    for var in result[1]:
                        postprocessing_info[var] = result[1][var]
        for heuristic in self.preprocessing_heuristics:
            if self.config ['heuristics'][heuristic.__name__[(heuristic.__name__).find("_") + 1:]]:
                result = heuristic(prompt)
                prompt = result[0]
                for var in result[1]:
                    postprocessing_info[var] = result[1][var]
        return [prompt, postprocessing_info]

    def apply_postprocessing(self, prompt: str, postprocessing_info: dict) -> str:
        """Apply postprocessing heuristics to the prompt based on the configuration."""
        for heuristic in self.postprocessing_heuristics:
            if self.config ['heuristics'][heuristic.__name__[(heuristic.__name__).find("_") + 1:]]:
                prompt = heuristic(prompt, postprocessing_info)
        return prompt

    def preprocessing_remove_commas(self, prompt: str):
        """Remove commas from the text."""
        return [prompt.replace(",", ""), {}]

    def preprocessing_replace_tags_with_placeholder(self, prompt: str):
        """Replace XML tags with a placeholder."""
        replaced_tags = re.findall(r"<[^>]*>", prompt)
        return [re.sub(r"<[^>]*>", " " + self.placeholder + " ", prompt),
                {"replaced_tags": replaced_tags, "placeholder": self.placeholder}]

    def postprocessing_replace_tags_with_placeholder(self, prompt: str, postprocessing_info: dict) -> str:
        """Replace placeholders with XML tags."""
        placeholder = postprocessing_info["placeholder"]
        if not placeholder:
            return prompt
        for tag in postprocessing_info["replaced_tags"]:
            prompt = prompt.replace(placeholder, f"{tag}", 1)
        # So if there are any excess placeholders, validate_response would catch tag count mismatch
        prompt = prompt.replace(placeholder, "<>")
        return prompt
