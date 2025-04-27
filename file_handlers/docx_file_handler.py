import docx
import re
import logging
from typing import Dict, List
from file_handlers.base_file_handler import BaseFileHandler
from docx.text.run import Run


class DOCXFileHandler(BaseFileHandler):
    TAG_PREFIX = "<RUN"
    TAG_SUFFIX = "/>"

    def _generate_tag(self, index: int) -> str:
        """Generate a unique tag for a text fragment."""
        return f"{self.TAG_PREFIX}{index}{self.TAG_SUFFIX}"

    def extract_text(self, filepath: str) -> str:
        """Extract text from DOCX, inserting tags before each text fragment, and returns a string for LLM and a map 'tag -> Run object'.
        """
        try:
            document = docx.Document(filepath)
            text_for_llm_parts = []
            run_index = 1

            for para in document.paragraphs:
                for run in para.runs:
                    tag = self._generate_tag(run_index)
                    text_for_llm_parts.append(tag + run.text)
                    run_index += 1

            full_text_for_llm = "".join(text_for_llm_parts)
            return full_text_for_llm

        except Exception as e:
            logging.error(f"Error extracting text/mapping from {filepath}: {e}")
            return ""

    def insert_text(self,
                                original_filepath: str,
                                processed_chunks: List[str],
                                output_filepath: str):
        """Update the text of fragments in the document based on the processed string with tags."""
        try:
            processed_text_with_tags = "".join(processed_chunks)
            logging.info(processed_text_with_tags)
            document = docx.Document(original_filepath)
            new_run_map: Dict[str, Run] = {}
            run_index = 1
            for para in document.paragraphs:
                 for run in para.runs:
                     tag = self._generate_tag(run_index)
                     new_run_map[tag] = run
                     run_index += 1

            tag_pattern = re.compile(f"({self.TAG_PREFIX}\\d+{self.TAG_SUFFIX})", re.DOTALL)

            parts = tag_pattern.split(processed_text_with_tags)

            processed_runs_count = 0
            missed_tags = set(new_run_map.keys())

            for i in range(1, len(parts), 2):
                tag = parts[i]
                text_after_tag = parts[i+1] if (i+1) < len(parts) else ""

                if tag in new_run_map:
                    run_object = new_run_map[tag]
                    run_object.text = text_after_tag
                    processed_runs_count += 1
                    missed_tags.discard(tag)
                else:
                    logging.warning(f"Tag '{tag}' found in LLM response but not in original document map. Skipping.")

            if missed_tags:
                logging.warning(f"{len(missed_tags)} original tags were not found in the LLM response. Their corresponding run texts were not updated.")
                logging.warning(f"Missing tags: {missed_tags}")

            document.save(output_filepath)

        except Exception as e:
            logging.error(f"Error inserting processed text into {output_filepath}: {e}")