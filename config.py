import json
import os


def load_config(config_file="config.json"):
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file}")
    with open(config_file, "r") as f:
        config_data = json.load(f)
    return config_data


config = load_config()

if "gemini_api_key" not in config:
    raise ValueError("Gemini API key is missing in the config file.")
GEMINI_API_KEY = config["gemini_api_key"]

if "model_name" not in config:
    raise ValueError("Model name is missing in the config file.")
MODEL_NAME = config["model_name"]

if "chunk_size" not in config:
    raise ValueError("Chunk size is missing in the config file.")
CHUNK_SIZE = config["chunk_size"]

if "output_dir" not in config:
    raise ValueError("Output directory is missing in the config file.")
OUTPUT_DIR = config["output_dir"]

if "main_prompt" not in config:
    raise ValueError("Main prompt is missing in the config file.")
MAIN_PROMPT = config["main_prompt"]
