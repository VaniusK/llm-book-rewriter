import os
from lxml import etree
import re

class FileManager:
    def __init__(self, processed_chunks_file="processed_chunks.txt", processed_chunks_count_file="processed_chunks_count.txt"):
        self.processed_chunks_file = processed_chunks_file
        self.processed_chunks_count_file = processed_chunks_count_file

    def insert_text_into_fb2(self, original_filepath, processed_chunks, output_filepath):
        """Replaces fb2's <body> with given text"""
        with open(original_filepath, 'r', encoding="utf-8") as input_file:
            with open(output_filepath, 'w', encoding="utf-8") as output_file:
                input_file_text = input_file.read()
                pattern = r"<body.*?>(.*?)</body>"
                flags = re.DOTALL | re.IGNORECASE
                input_file_text = re.sub(pattern, f"{processed_chunks}", input_file_text, flags=flags)
                output_file.write(input_file_text)

    def extract_text_and_tags_from_fb2(self, filepath):
        """Extracts text and tags from fb2 file"""
        tree = etree.parse(filepath)
        root = tree.getroot()

        namespaces = {'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'}

        # Function to recursively process elements
        def process_element(element, depth=0):
            text_with_tags = ""

            tag_name = etree.QName(element).localname
            if tag_name == "binary":
                return text_with_tags
            text_with_tags += f"<{tag_name}>"
            if element.text:
                text_with_tags += f"{element.text}"
            for child in element:
                text_with_tags += process_element(child, depth + 1)
            text_with_tags += f"</{tag_name}>"
            if element.tail:
                text_with_tags += f"{element.tail}"

            return text_with_tags

        body = root.xpath('.//fb:body', namespaces=namespaces)[0]
        all_text_with_tags = process_element(body)

        return all_text_with_tags

    def save_processed_chunks(self, chunk):
        with open(self.processed_chunks_file, "a") as file:
            file.write(chunk)

    def clear_processed_chunks(self):
        with open(self.processed_chunks_file, "w") as file:
            file.write("")

    def load_processed_chunks(self):
        if not os.path.exists(self.processed_chunks_file):
            return ""
        with open(self.processed_chunks_file, "r") as file:
            return file.read()

    def save_processed_chunks_count(self, chunk_count):
        with open(self.processed_chunks_count_file, "w") as file:
            file.write(str(chunk_count))

    def load_processed_chunks_count(self):
        if not os.path.exists(self.processed_chunks_count_file):
            return 0
        with open(self.processed_chunks_count_file, "r") as file:
            f = file.read()
            return int(f) if f else -1