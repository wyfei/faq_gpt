"""Configuration class to store the state of bools for different scripts access."""
import os
from colorama import Fore

from config.singleton import Singleton

import openai

from dotenv import load_dotenv

load_dotenv(verbose=True)


class Config(metaclass=Singleton):
    """
    Configuration class to store the state of bools for different scripts access.
    """

    def __init__(self) -> None:
        """Initialize the Config class"""
        self.debug_mode = False
        self.docx_file = os.getenv("DOCX_FILE")
        self.fast_llm_model = os.getenv("FAST_LLM_MODEL", "gpt-3.5-turbo")
        self.smart_llm_model = os.getenv("SMART_LLM_MODEL", "gpt-4")
        self.fast_stream_max_token = int(os.getenv("FAST_STREAM_MAX_TOKEN", 512))

        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.temperature = float(os.getenv("TEMPERATURE", "1"))

        self.memory_backend = os.getenv("MEMORY_BACKEND", "faiss")
        # Initialize the OpenAI API client
        openai.api_key = self.openai_api_key

        
    def set_docx_file(self, value: str) -> None:
        """Set the fast LLM model value."""
        self.docx_file = value
        
    def set_fast_llm_model(self, value: str) -> None:
        """Set the fast LLM model value."""
        self.fast_llm_model = value

    def set_smart_llm_model(self, value: str) -> None:
        """Set the smart LLM model value."""
        self.smart_llm_model = value

    def set_fast_stream_max_token(self, value: int) -> None:
        """Set the fast token limit value."""
        self.fast_stream_max_token = value

    def set_openai_api_key(self, value: str) -> None:
        """Set the OpenAI API key value."""
        self.openai_api_key = value

    def set_temperature(self, value: int) -> None:
        """Set the OpenAI temperature value."""
        self.temperature = value
        
    def set_debug_mode(self, value: bool) -> None:
        """Set the debug mode value."""
        self.debug_mode = value


def check_openai_api_key() -> None:
    """Check if the OpenAI API key is set in config.py or as an environment variable."""
    cfg = Config()
    if not cfg.openai_api_key:
        print(
            Fore.RED
            + "Please set your OpenAI API key in .env or as an environment variable."
        )
        print("You can get your key from https://beta.openai.com/account/api-keys")
        exit(1)
