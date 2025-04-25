from imports import *

class BaseLLM(ABC):
    @abstractmethod
    def __init__(self, model_name: str, api_key: str):
        """
        Initializes the LLM with the given model name and API key.

        Args:
            model_name (str): The name of the LLM model to use.
            api_key (str): The API key for accessing the LLM.
        """
        pass

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generates text based on the given prompt.

        Args:
            prompt (str): The input prompt for text generation.
        Returns:
            str: The generated text.
        """
        pass