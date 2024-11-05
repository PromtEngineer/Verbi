# voice_assistant/api_key_manager.py

from voice_assistant.config import Config

API_KEY_MAPPING= {
    "transcription":{
        "openai": Config.OPENAI_API_KEY,
        "groq": Config.GROQ_API_KEY,
        "deepgram": Config.DEEPGRAM_API_KEY
    },
    "response":{
        "openai":Config.OPENAI_API_KEY,
        "groq": Config.GROQ_API_KEY
    },
    "tts": {
        "openai": Config.OPENAI_API_KEY,
        "deepgram":Config.DEEPGRAM_API_KEY,
        "elevenlabs": Config.ELEVENLABS_API_KEY
    }
}

def get_api_key(service, model):
    """
    Select the API key for the specified service and model
    
    Returns:
    str: The API key for the transcription, response or tts service.
    """
    return API_KEY_MAPPING.get(service, {}).get(model)

def get_transcription_api_key():
    """
    Select the correct API key for transcription based on the configured model.
    
    Returns:
    str: The API key for the transcription service.
    """
    return get_api_key("transcription", Config.TRANSCRIPTION_MODEL)

def get_response_api_key():
    """
    Select the correct API key for response generation based on the configured model.
    
    Returns:
    str: The API key for the response generation service.
    """
    return get_api_key("response", Config.RESPONSE_MODEL)

def get_tts_api_key():
    """
    Select the correct API key for text-to-speech based on the configured model.
    
    Returns:
    str: The API key for the TTS service.
    """
    return get_api_key("tts", Config.TTS_MODEL)