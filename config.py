import os
import yaml
import collections.abc
from typing import Dict, Any

def load_config(config_file: str):
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
        return config_data
    return {}

def deep_merge_dicts(base_dict: Dict[Any, Any], override_dict: Dict[Any, Any]):
    """
    Merging two dictionaries with second one getting the priority
    """
    for key, value in override_dict.items():
        if (key in base_dict and
                isinstance(base_dict[key], collections.abc.Mapping) and
                isinstance(value, collections.abc.Mapping)):
            deep_merge_dicts(base_dict[key], dict(value))
        else:
            base_dict[key] = value
    return base_dict

config = deep_merge_dicts(load_config("config.yaml"), load_config("config_local.yaml"))