from llm_providers.base_llm import BaseLLM
from openai import AsyncOpenAI

class OpenaiError(Exception):
    """Raised when LLM generation fails (e.g., quota exceeded)."""
    pass


class Gemini(BaseLLM):
    """A class for Gemini LLM provider."""

    def __init__(self, model_name: str, api_key: str, config: dict[any, any]):
        """Initialize the LLM with the given model name and API key."""
        print(api_key)
        self.client = AsyncOpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=api_key,
        )
        self.model = model_name
        self.config = config

    async def generate(self, prompt: str) -> str:
        """Generate text based on the given prompt."""
        completion = await self.client.chat.completions.create(
            model=self.model,
            reasoning_effort="minimal",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }, 
                {
                    "role": "user",
                    "content": "Начните вычитку текста."
                }
            ]
        )
        if hasattr(completion, 'error'):
            if completion.error:
                raise OpenaiError(completion.error["message"])
        if not hasattr(completion.choices[0].message, 'content'):
            raise OpenaiError(completion.__dict__)
        else:
            return completion.choices[0].message.content
