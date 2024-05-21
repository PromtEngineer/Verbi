# voice_assistant/config.py

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    """
    Configuration class to hold the model selection and API keys.
    
    Attributes:
    TRANSCRIPTION_MODEL (str): The model to use for transcription ('openai', 'groq', 'deepgram', 'local').
    RESPONSE_MODEL (str): The model to use for response generation ('openai', 'groq', 'local').
    TTS_MODEL (str): The model to use for text-to-speech ('openai', 'deepgram', 'local').
    OPENAI_API_KEY (str): API key for OpenAI services.
    GROQ_API_KEY (str): API key for Groq services.
    DEEPGRAM_API_KEY (str): API key for Deepgram services.
    LOCAL_MODEL_PATH (str): Path to the local model.
    """
    # Model selection
    TRANSCRIPTION_MODEL = 'deepgram'  # possible values: openai, groq
    RESPONSE_MODEL = 'groq'       # possible values: openai, groq
    TTS_MODEL = 'deepgram'        # possible values: openai, deepgram

    # API keys and paths
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH")

    @staticmethod
    def validate_config():
        """
        Validate the configuration to ensure all necessary environment variables are set.
        
        Raises:
        ValueError: If a required environment variable is not set.
        """
        if Config.TRANSCRIPTION_MODEL not in ['openai', 'groq', 'deepgram', 'local']:
            raise ValueError("Invalid TRANSCRIPTION_MODEL. Must be one of ['openai', 'groq', 'deepgram', 'local']")
        if Config.RESPONSE_MODEL not in ['openai', 'groq', 'local']:
            raise ValueError("Invalid RESPONSE_MODEL. Must be one of ['openai', 'groq', 'local']")
        if Config.TTS_MODEL not in ['openai', 'deepgram', 'local']:
            raise ValueError("Invalid TTS_MODEL. Must be one of ['openai', 'deepgram', 'local']")

        if Config.TRANSCRIPTION_MODEL == 'openai' and not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for OpenAI models")
        if Config.TRANSCRIPTION_MODEL == 'groq' and not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required for Groq models")
        if Config.TRANSCRIPTION_MODEL == 'deepgram' and not Config.DEEPGRAM_API_KEY:
            raise ValueError("DEEPGRAM_API_KEY is required for Deepgram models")

        if Config.RESPONSE_MODEL == 'openai' and not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for OpenAI models")
        if Config.RESPONSE_MODEL == 'groq' and not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required for Groq models")

        if Config.TTS_MODEL == 'openai' and not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for OpenAI models")
        if Config.TTS_MODEL == 'deepgram' and not Config.DEEPGRAM_API_KEY:
            raise ValueError("DEEPGRAM_API_KEY is required for Deepgram models")
