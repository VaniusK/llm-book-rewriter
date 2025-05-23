import yaml
import collections.abc
from pathlib import Path

def load_config(config_file: Path):
    """Load config from .yaml file."""
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
        return config_data
    return {}

def deep_merge_dicts(base_dict: dict[any, any], override_dict: dict[any, any]):
    """Merge two dictionaries with second one getting the priority."""
    for key, value in override_dict.items():
        if (key in base_dict and
                isinstance(base_dict[key], collections.abc.Mapping) and
                isinstance(value, collections.abc.Mapping)):
            deep_merge_dicts(base_dict[key], dict(value))
        else:
            base_dict[key] = value
    return base_dict

config_filename = "config.yaml"
config_local_filename = "config_local.yaml"



config = deep_merge_dicts(load_config(Path(config_filename)), load_config(Path(config_local_filename)))