import os
import yaml

def load_config(config_file="config.yaml"):
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
        return config_data
    return {}

config = load_config()
config_local = load_config("config_local.yaml")
if "google" in config_local:
    config["google"]["api_key"] = config_local["google"]["api_key"]
