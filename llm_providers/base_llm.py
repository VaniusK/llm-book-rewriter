from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def __init__(self, model_name: str, api_key: str):
        """Initialize the LLM with the given model name and API key."""
        pass

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate text based on the given prompt."""
        pass