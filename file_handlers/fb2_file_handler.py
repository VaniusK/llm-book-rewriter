from typing import List
import re
from lxml import etree
from file_handlers.base_file_handler import BaseFileHandler

class FB2FileHandler(BaseFileHandler):
    def insert_text(self, original_filepath: str, processed_chunks: List[str], output_filepath: str):
        """Replace fb2's <body> with given text."""
        with open(original_filepath, 'r', encoding="utf-8") as input_file:
            with open(output_filepath, 'w', encoding="utf-8") as output_file:
                input_file_text = input_file.read()
                pattern = r"<body.*?>(.*?)</body>"
                flags = re.DOTALL | re.IGNORECASE
                input_file_text = re.sub(pattern, f"{processed_chunks}", input_file_text, flags=flags)
                output_file.write(input_file_text)

    def extract_text(self, filepath: str):
        """Extract text and tags from fb2 file."""
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
            child_count = 0
            for child in element:
                child_count += 1
                text_with_tags += process_element(child, depth + 1)
            if child_count or element.text:
                text_with_tags += f"</{tag_name}>"
            if element.tail:
                text_with_tags += f"{element.tail}"

            return text_with_tags

        body = root.xpath('.//fb:body', namespaces=namespaces)[0]
        all_text_with_tags = process_element(body)

        return all_text_with_tags
