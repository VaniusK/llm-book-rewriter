from typing import List
import re
from lxml import etree
import html
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
        try:
            tree = etree.parse(filepath)
        except etree.XMLSyntaxError as e:
            print(f"Error parsing XML: {e}")
            return f"<error>Could not parse XML: {e}</error>"
        root = tree.getroot()

        def process_element(element: etree.Element, root_nsmap):
            parts = []

            qname_element = etree.QName(element)
            tag_localname = qname_element.localname
            element_uri = qname_element.namespace

            element_prefix = None
            if element_uri is not None:
                for p, u in element.nsmap.items():
                    if u == element_uri:
                        element_prefix = p
                        break
                if element_prefix is None:
                    for p, u in root_nsmap.items():
                        if u == element_uri:
                            element_prefix = p
                            break

            tag_display_name = tag_localname
            if element_prefix is not None:
                if element_prefix is not None:
                    tag_display_name = f"{element_prefix}:{tag_localname}"

            if tag_localname == "binary" and element_uri == 'http://www.gribuser.ru/xml/fictionbook/2.0':
                return ""

            parts.append(f"<{tag_display_name}")

            for attr_name_qualified, attr_value in element.attrib.items():
                qname_attr = etree.QName(attr_name_qualified)
                attr_uri = qname_attr.namespace
                attr_localname = qname_attr.localname

                attr_prefix = None
                if attr_uri is not None:
                    for p, u in element.nsmap.items():
                        if u == attr_uri:
                            attr_prefix = p
                            break
                    if attr_prefix is None:
                        for p, u in root_nsmap.items():
                            if u == attr_uri:
                                attr_prefix = p
                                break

                attr_display_name = attr_localname
                if attr_prefix is not None:
                    if attr_prefix is not None:
                        attr_display_name = f"{attr_prefix}:{attr_localname}"
                elif attr_uri is not None:
                    attr_display_name = attr_localname  # Fallback if namespaced but prefix not found

                parts.append(f' {attr_display_name}="{html.escape(attr_value, quote=True)}"')

            if not element.text and len(element) == 0:
                parts.append("/>")
            else:
                parts.append(">")
                if element.text:
                    parts.append(html.escape(element.text))

                for child in element:
                    parts.append(process_element(child, root_nsmap))

                parts.append(f"</{tag_display_name}>")

            if element.tail:
                parts.append(html.escape(element.tail))

            return "".join(parts)

        body_elements = root.xpath('.//fb:body', namespaces={'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'})
        if not body_elements:
            body_elements = root.xpath('.//body[namespace-uri()="http://www.gribuser.ru/xml/fictionbook/2.0"]')
            if not body_elements:
                body_elements = root.xpath(
                    "//*[local-name()='body' and namespace-uri()='http://www.gribuser.ru/xml/fictionbook/2.0']")
                if not body_elements:
                    return "<error>No body element found with FictionBook namespace.</error>"

        body = body_elements[0]
        all_text_with_tags = process_element(body, root.nsmap)

        return all_text_with_tags
