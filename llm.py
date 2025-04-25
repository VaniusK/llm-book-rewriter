from imports import *
from config import config

class LLM:
    """
    Factory class for creating LLM instances.

    This class dynamically imports and instantiates LLM classes from the llm_providers package.
    """
    def __init__(self, provider : str):
        self.provider = provider
        self.llm = self.get_llm()

    def get_llm(self):
        try:
            module = importlib.import_module("llm_providers." + self.provider)
            llm_class = getattr(module, self.provider.capitalize())
            llm_instance = llm_class(config[self.provider]['model'], config[self.provider]['api_key'])
            return llm_instance
        except ImportError:
            raise ImportError(f"Could not import module llm_providers.{self.provider}")
        except AttributeError:
            raise AttributeError(f"Class {self.provider.capitalize()} not found in module llm_providers.{self.provider}")
        except Exception as e:
             raise Exception(f"An error occurred while creating LLM instance: {e}")