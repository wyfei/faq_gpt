import json
import re
from abc import abstractmethod
from typing import Dict, NamedTuple

from langchain.schema import BaseOutputParser


class GPTAction(NamedTuple):
    name: str
    args: Dict

class TransferAction(NamedTuple):
    original: str
    retrieval: str
    similarity: float

    
class BaseGPTOutputParser(BaseOutputParser):
    @abstractmethod
    def parse(self, text: str) -> GPTAction:
        """Return GPTAction"""


def preprocess_json_input(input_str: str) -> str:
    # Replace single backslashes with double backslashes,
    # while leaving already escaped ones intact
    corrected_str = re.sub(
        r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r"\\\\", input_str
    )
    return corrected_str


class GPTOutputParser(BaseGPTOutputParser):
    def parse(self, text: str) -> GPTAction:
        try:
            parsed = json.loads(text, strict=False)
        except json.JSONDecodeError:
            preprocessed_text = preprocess_json_input(text)
            try:
                parsed = json.loads(preprocessed_text, strict=False)
            except Exception:
                return GPTAction(
                    name="ERROR",
                    args={"error": f"Could not parse invalid json: {text}"},
                )
        try:
            return GPTAction(
                name=parsed["command"]["name"],
                args=parsed["command"]["args"],
            )
        except (KeyError, TypeError):
            # If the command is null or incomplete, return an erroneous tool
            return GPTAction(
                name="ERROR", args={"error": f"Incomplete command args: {parsed}"}
            )
            
class TransferOutputParser(BaseGPTOutputParser):
    def parse(self, text: str) -> TransferAction:
        try:
            parsed = json.loads(text, strict=False)
        except json.JSONDecodeError:
            preprocessed_text = preprocess_json_input(text)
            try:
                parsed = json.loads(preprocessed_text, strict=False)
            except Exception:
                return TransferAction(
                    original = text,
                    retrieval = text,
                    similarity = 1
                )
        try:
            return TransferAction(
                original = parsed["user_question"],
                retrieval = parsed["retrieval_question"],
                similarity = parsed["similarity"]
            )
        except (KeyError, TypeError):
            # If the command is null or incomplete, return an erroneous tool
            return TransferAction(
                original = text,
                retrieval = text,
                similarity = 1
            )