from typing import List, Any, Dict
import re
import logging
from config import config

class HeuristicApplier:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.preprocessing_original_heuristics = [self.preprocessing_remove_commas]
        self.preprocessing_heuristics = [self.preprocessing_replace_tags_with_placeholder]
        self.postprocessing_heuristics = [self.postprocessing_replace_tags_with_placeholder]
        self.possible_placeholders = ["@", "#", "$", "%", "^", "&", "*", "~", "`", "@@", "@#", "@$", "@%"]

    def apply_preprocessing(self, prompt: str, is_original: bool) -> List[Any]:
        """Apply preprocessing heuristics to the prompt based on the configuration."""
        postprocessing_info = dict()
        if is_original:
            for heuristic in self.preprocessing_original_heuristics:
                if config['heuristics'][heuristic.__name__[(heuristic.__name__).find("_") + 1:]]:
                    result = heuristic(prompt)
                    prompt = result[0]
                    for var in result[1]:
                        postprocessing_info[var] = result[1][var]
        for heuristic in self.preprocessing_heuristics:
            if config['heuristics'][heuristic.__name__[(heuristic.__name__).find("_") + 1:]]:
                result = heuristic(prompt)
                prompt = result[0]
                for var in result[1]:
                    postprocessing_info[var] = result[1][var]
        return [prompt, postprocessing_info]

    def apply_postprocessing(self, prompt: str, postprocessing_info: Dict) -> str:
        """Apply postprocessing heuristics to the prompt based on the configuration."""
        for heuristic in self.postprocessing_heuristics:
            if config['heuristics'][heuristic.__name__[(heuristic.__name__).find("_") + 1:]]:
                prompt = heuristic(prompt, postprocessing_info)
        return prompt

    def preprocessing_remove_commas(self, prompt: str):
        """Remove commas from the text."""
        return [prompt.replace(",", ""), {}]

    def preprocessing_replace_tags_with_placeholder(self, prompt: str):
        """Replace XML tags with a placeholder."""
        replaced_tags = []
        for placeholder in self.possible_placeholders:
            if placeholder not in prompt:
                replaced_tags = re.findall(r"<(.+?)>", prompt)
                return [re.sub(r"<.+?>", placeholder, prompt), {"replaced_tags": replaced_tags, "placeholder": placeholder}]
        self.logger.warning(f"Couldn't apply the replace_tags_with_placeholder heuristic: no available placeholder found")
        return [prompt, {"replaced_tags": replaced_tags, "placeholder": ""}]

    def postprocessing_replace_tags_with_placeholder(self, prompt: str, postprocessing_info: Dict) -> str:
        """Replace placeholders with XML tags."""
        placeholder = postprocessing_info["placeholder"]
        if not placeholder:
            return prompt
        for tag in postprocessing_info["replaced_tags"]:
            prompt = prompt.replace(placeholder, f"<{tag}>", 1)
        # So if there are any excess placeholders, validate_response would catch tag count mismatch
        prompt = prompt.replace(placeholder, "<>")
        return prompt


