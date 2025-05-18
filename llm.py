import importlib

class LLM:
    """
    Factory class for creating LLM instances.

    This class dynamically imports and instantiates LLM classes from the llm_providers package.
    """
    def __init__(self, config: dict[any, any]):
        """Initialize the LLM based on config."""
        self.provider = config["processing"]["provider"]
        self.config = config
        self.llm = self.get_llm()

    def get_llm(self) -> object:
        """Return llm class based on provider name."""
        module_name = "llm_providers." + self.provider
        class_name = self.provider.capitalize()

        try:
            module = importlib.import_module(module_name)
            llm_class = getattr(module, class_name)
            llm_instance = llm_class(self.config[self.provider]['model'], self.config[self.provider]['api_key'], self.config)
            return llm_instance
        except ImportError:
            raise ImportError(f"Could not import module {module_name}")
        except AttributeError:
            raise AttributeError(f"Class {class_name} not found in module {module_name}")
        except Exception as e:
             raise Exception(f"An error occurred while creating LLM instance: {e}")