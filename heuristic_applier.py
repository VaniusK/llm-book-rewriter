from config import config
import re
import logging

class HeuristicApplier:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.preprocessing_heuristics = [self.preprocessing_remove_commas, self.preprocessing_replace_tags_with_placeholder]
        self.postprocessing_heuristics = [self.postprocessing_replace_tags_with_placeholder]
        self.possible_placeholders = ["@", "#", "$", "%", "^", "&", "*", "~", "`", "@@", "@#", "@$", "@%"]
        self.replaced_tags = []
        self.chosen_placeholder = ""

    def apply_preprocessing(self, prompt: str) -> str:
        """Apply preprocessing heuristics to the prompt based on the configuration."""
        for heuristic in self.preprocessing_heuristics:
            if config['heuristics'][heuristic.__name__[(heuristic.__name__).find("_") + 1:]]:
                prompt = heuristic(prompt)
        return prompt

    def apply_postprocessing(self, prompt: str) -> str:
        """Apply postprocessing heuristics to the prompt based on the configuration."""
        for heuristic in self.postprocessing_heuristics:
            if config['heuristics'][heuristic.__name__[(heuristic.__name__).find("_") + 1:]]:
                prompt = heuristic(prompt)
        return prompt

    def preprocessing_remove_commas(self, prompt: str) -> str:
        """Remove commas from the text."""
        return prompt.replace(",", "")

    def preprocessing_replace_tags_with_placeholder(self, prompt: str) -> str:
        """Replace XML tags with a placeholder."""
        if not hasattr(self, 'replaced_tags'):
            self.replaced_tags = []

        for placeholder in self.possible_placeholders:
            if placeholder not in prompt:
                self.replaced_tags = re.findall(r"<(.+?)>", prompt)
                self.chosen_placeholder = placeholder
                return re.sub(r"<.+?>", placeholder, prompt)
        self.logger.warning(f"Couldn't apply the replace_tags_with_placeholder heuristic: no available placeholder found")
        return prompt

    def postprocessing_replace_tags_with_placeholder(self, prompt: str) -> str:
        """Replace placeholders with XML tags."""
        placeholder = self.chosen_placeholder
        if not placeholder:
            return prompt
        for tag in self.replaced_tags:
            prompt = prompt.replace(placeholder, f"<{tag}>", 1)
        prompt.replace(placeholder, "<>")
        return prompt


