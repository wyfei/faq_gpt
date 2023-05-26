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
        self.sess_data = os.getenv("SESSDATA")
        self.bili_jct = os.getenv("BILI_JCT")
        self.buvid3 = os.getenv("BUVID3")
        self.rasa_nlu_api = os.getenv("RASA_NLU_API")
        self.rasa_rest_api = os.getenv("RASA_REST_API")
        
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
        
    def set_sess_data(self, value: str) -> None:
        self.sess_data = value
        
    def set_bili_jct(self, value: str) -> None:
        self.bili_jct = value
        
    def set_buvid3(self, value: str) -> None:
        self.buvid3 = value
        
    def set_rasa_nlu_api(self, value: str) -> None:
        self.rasa_nlu_api = value
        
    def set_rasa_rest_api(self, value: str) -> None:
        self.rasa_rest_api = value


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
