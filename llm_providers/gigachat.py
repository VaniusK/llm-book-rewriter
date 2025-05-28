from llm_providers.base_llm import BaseLLM
from openai import AsyncOpenAI
import uuid
import requests

class OpenaiError(Exception):
    """Raised when LLM generation fails (e.g., quota exceeded)."""
    pass


class Gigachat(BaseLLM):
    """A class for Gigachat(Sber) LLM provider."""

    def __init__(self, model_name: str, authorization_key: str, config: dict[any, any]):
        """Initialize the LLM with the given model name and API key."""
        self.access_token = self._get_access_token(config["gigachat"]["scope"], authorization_key)
        self.client = AsyncOpenAI(
            base_url="https://gigachat.devices.sberbank.ru/api/v1",
            api_key=self.access_token,
        )
        self.model = model_name
        self.config = config

    def _get_access_token(self, scope: str, authorization_key: str):
        """Get access token for Gigachat API."""
        token_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        rq_uid = str(uuid.uuid4())

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": rq_uid,
            "Authorization": f"Basic {authorization_key}",
        }
        data = {
            "scope": scope,
        }

        try:
            response = requests.post(token_url, headers=headers, data=data)
            token_data = response.json()
            return token_data["access_token"]
        except:
            raise OpenaiError("Couldn't get Gigachat access token")

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
