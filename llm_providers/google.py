from google import genai
from google.genai import types as genai_types
from llm_providers.base_llm import BaseLLM
from config import config

class Google(BaseLLM):
    def __init__(self, model_name: str, api_key: str):
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
        if "2.5-flash" in model_name:
            self.model_config.thinking_config=genai_types.ThinkingConfig(thinking_budget=config["google"]["thinking_budget"])

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=[prompt],
            config=self.model_config
        )
        return response.text if response.text else ""