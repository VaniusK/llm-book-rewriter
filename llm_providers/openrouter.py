from llm_providers.base_llm import BaseLLM
from openai import AsyncOpenAI

class OpenaiError(Exception):
    pass

class Openrouter(BaseLLM):
    def __init__(self, model_name: str, api_key: str):
        """Initialize the LLM with the given model name and API key."""
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = model_name


    async def generate(self, prompt: str) -> str:
        """Generate text based on the given prompt."""
        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        if hasattr(completion, 'error'):
            if completion.error:
                raise OpenaiError(completion.error["message"])
        else:
            return completion.choices[0].message.content