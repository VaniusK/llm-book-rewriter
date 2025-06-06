import importlib

class FileHandler:
    """
    Factory class for creating file handler instances.

    This class dynamically imports and instantiates file handler classes.
    """
    def __init__(self, file_type : str, config: dict[any, any]):
        """Initialize the FileHandler based on file_type and config."""
        self.file_type = file_type
        self.config = config
        self.file_handler = self.get_file_handler()

    def get_file_handler(self) -> object:
        """Return file_handler class based on file_type."""
        module_name = f"file_handlers.{self.file_type}_file_handler"
        class_name = f"{self.file_type.upper()}FileHandler"

        try:
            module = importlib.import_module(module_name)
            file_handler_class = getattr(module, class_name)
            file_handler_instance = file_handler_class(self.config)
            return file_handler_instance
        except ImportError:
            raise ImportError(f"Could not import module {module_name}")
        except AttributeError:
            raise AttributeError(f"Class {class_name} not found in module {module_name}")
        except Exception as e:
            raise Exception(f"An error occurred while creating file handler instance: {e}")