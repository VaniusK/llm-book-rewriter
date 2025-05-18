from google import genai
from google.genai import types as genai_types
from llm_providers.base_llm import BaseLLM


class Gemini(BaseLLM):
    """A class for Gemini(Google) LLM provider."""

    def __init__(self, model_name: str, api_key: str, config: dict[any, any]):
        """
        Initializes the LLM with the given model name and API key.
        Disables safety filters to avoid responses being blocked.
        2.5-flash and potentially newer models require thinking_config
        """
        self.client = genai.Client(api_key=api_key)
        self.model = model_name
        self.safety_settings = [
            genai_types.SafetySetting(
                category=genai_types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=genai_types.HarmBlockThreshold.BLOCK_NONE,
            ),
            genai_types.SafetySetting(
                category=genai_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=genai_types.HarmBlockThreshold.BLOCK_NONE,
            ),
            genai_types.SafetySetting(
                category=genai_types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=genai_types.HarmBlockThreshold.BLOCK_NONE,
            ),
            genai_types.SafetySetting(
                category=genai_types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=genai_types.HarmBlockThreshold.BLOCK_NONE,
            ),
        ]
        self.model_config = genai_types.GenerateContentConfig(
            safety_settings=self.safety_settings,
            temperature=1,
            max_output_tokens=65000, # Reasoning counts as output
            top_p=0.95,
            top_k=64,
        )
        self.config = config
        if "2.5-flash" in model_name:
            self.model_config.thinking_config=genai_types.ThinkingConfig(thinking_budget=self.config["gemini"]["thinking_budget"])

    async def generate(self, prompt: str) -> str:
        """Generate text based on the given prompt."""
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=[prompt],
            config=self.model_config
        )
        return response.text if response.text else ""