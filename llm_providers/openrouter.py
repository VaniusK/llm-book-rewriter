from google.genai.errors import APIError

from llm_providers.base_llm import BaseLLM
from openai import AsyncOpenAI

class OpenaiError(Exception):
    pass

class Openrouter(BaseLLM):
    def __init__(self, model_name: str, api_key: str):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = model_name


    async def generate(self, prompt: str) -> str:
        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        if completion.error:
            raise OpenaiError(completion.error["message"])
        return completion.choices[0].message.content