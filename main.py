import os
from google import genai
import time
from google.genai import types as genai_types
from file_manager import FileManager
import config

GEMINI_API_KEY = config.GEMINI_API_KEY
MODEL_NAME = config.MODEL_NAME
CHUNK_SIZE = config.CHUNK_SIZE
OUTPUT_DIR = config.OUTPUT_DIR


model = MODEL_NAME
client = genai.Client(
    api_key=GEMINI_API_KEY
)

def split_into_chunks(text, chunk_size):
    """Splits text into chunks of(roughly) given size, considering tag endings."""
    chunks = []
    current_chunk = ""
    current_chunk_size = 0
    processed_size = 0

    for char in text:
        segment_size = 1
        current_chunk += char
        current_chunk_size += segment_size

        if current_chunk_size >= chunk_size and char == ">" and len(text) - processed_size >= chunk_size // 10:
            chunks.append(current_chunk)
            current_chunk = ""
            processed_size += current_chunk_size
            current_chunk_size = 0

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def generate_with_gemini(client, model, prompt, text_chunk):
    """Sends request to Gemini with given prompt and settings, returns response"""

    full_prompt = f"""{prompt}

**Фрагмент текста:**
{text_chunk}

**Инструкции:**
1. Выполните задачу, указанную в основном запросе, над предоставленным текстовым фрагментом.
2. Выведите только обработанный текстовый фрагмент, избегайте добавления каких-либо дополнительных вводных или заключительных утверждений.
3. Не добавляйте/не удаляйте/не изменяйте пустые символы (разрывы строк, пробелы, табуляции и т. д.). Сохраняйте их в том виде, в каком они есть, включая края, перед тегами и т. д.
4. Не добавляйте/не удаляйте/не изменяйте теги.
"""

    safety_settings = [
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
    response = client.models.generate_content(
        model=model,
        contents=[full_prompt],
        config=genai_types.GenerateContentConfig(
            safety_settings=safety_settings,
            temperature=0
        )
    )
    return response.text if response.text else ""

def format_response(original_chunk, processed_chunk):
    """Ensures correct special symbol(\n, \t, whitespace, etc) usage on chunk edges
    by copying them from original chunk to processed one"""
    original_start_whitespace = ""
    original_end_whitespace = ""

    # Extract leading whitespace
    i = 0
    while i < len(original_chunk) and original_chunk[i].isspace():
        original_start_whitespace += original_chunk[i]
        i += 1

    # Extract trailing whitespace
    i = len(original_chunk) - 1
    while i >= 0 and original_chunk[i].isspace():
        original_end_whitespace = original_chunk[i] + original_end_whitespace
        i -= 1

    # Apply whitespace to processed chunk
    formatted_chunk = original_start_whitespace + processed_chunk.strip() + original_end_whitespace
    return formatted_chunk


def process_fb2_book(filepath: str, prompt: str, file_manager: FileManager):
    """Processes fb2 book by modifying each chunk with Gemini"""
    print(f"Processing: {filepath}")
    book_name = filepath[:-4]
    output_filepath = os.path.join(OUTPUT_DIR, f"{book_name}_rewritten.fb2")

    segments = file_manager.extract_text_and_tags_from_fb2(filepath)
    if not segments:
        print("Skipping: Could not extract text and tags.")
        return
    chunks = split_into_chunks(segments, CHUNK_SIZE)

    processed_chunks = [file_manager.load_processed_chunks()]
    chunks_processed = file_manager.load_processed_chunks_count()
    for i in range(chunks_processed + 1, len(chunks)):
        chunk = chunks[i]
        start_time = time.time()
        print(f"  Processing chunk {i + 1}/{len(chunks)}...")
        processed_chunk_text = chunk

        try:
            processed_chunk_text = generate_with_gemini(client, model, prompt, chunk)
            processed_chunk_text = format_response(chunk, processed_chunk_text)

        except Exception as e:
            print(e)
            print("Couldn't process the chunk, retrying")
            i -= 1
            continue

        processed_chunks.append(processed_chunk_text)
        file_manager.save_processed_chunks(processed_chunk_text)
        file_manager.save_processed_chunks_count(i)
        print(f"Chunk processed in {time.time() - start_time} seconds")
        file_manager.insert_text_into_fb2(filepath, ''.join(processed_chunks), output_filepath)
        print(f"Saved current progress to {output_filepath}")
    file_manager.clear_processed_chunks()
    file_manager.save_processed_chunks_count(-1)
    print(f"Processed {filepath}")



if __name__ == "__main__":
    main_prompt = config.MAIN_PROMPT

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_manager = FileManager()

    # Process all FB2 files in the input directory
    for filename in os.listdir("."):
        if filename.endswith(".fb2"):
            process_fb2_book(filename, main_prompt, file_manager)
