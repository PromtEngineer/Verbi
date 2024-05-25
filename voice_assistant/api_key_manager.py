# voice_assistant/api_key_manager.py

from voice_assistant.config import Config

def get_transcription_api_key():
    """
    Select the correct API key for transcription based on the configured model.
    
    Returns:
    str: The API key for the transcription service.
    """
    if Config.TRANSCRIPTION_MODEL == 'openai':
        return Config.OPENAI_API_KEY
    elif Config.TRANSCRIPTION_MODEL == 'groq':
        return Config.GROQ_API_KEY
    elif Config.TRANSCRIPTION_MODEL == 'deepgram':
        return Config.DEEPGRAM_API_KEY
    return None

def get_response_api_key():
    """
    Select the correct API key for response generation based on the configured model.
    
    Returns:
    str: The API key for the response generation service.
    """
    if Config.RESPONSE_MODEL == 'openai':
        return Config.OPENAI_API_KEY
    elif Config.RESPONSE_MODEL == 'groq':
        return Config.GROQ_API_KEY
    return None

def get_tts_api_key():
    """
    Select the correct API key for text-to-speech based on the configured model.
    
    Returns:
    str: The API key for the TTS service.
    """
    if Config.TTS_MODEL == 'openai':
        return Config.OPENAI_API_KEY
    elif Config.TTS_MODEL == 'deepgram':
        return Config.DEEPGRAM_API_KEY
    elif Config.TTS_MODEL == 'elevenlabs':
        return Config.ELEVENLABS_API_KEY
    return None
