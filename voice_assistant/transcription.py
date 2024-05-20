# voice_assistant/transcription.py

from openai import OpenAI
from groq import Groq
from deepgram import Deepgram
import logging

def transcribe_audio(model, api_key, audio_file_path, local_model_path=None):
    """
    Transcribe an audio file using the specified model.
    
    Args:
    model (str): The model to use for transcription ('openai', 'groq', 'deepgram', 'local').
    api_key (str): The API key for the transcription service.
    audio_file_path (str): The path to the audio file to transcribe.
    local_model_path (str): The path to the local model (if applicable).

    Returns:
    str: The transcribed text.
    """
    try:
        if model == 'openai':
            client = OpenAI(api_key=api_key)
            with open(audio_file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcription.text
        elif model == 'groq':
            client = Groq(api_key=api_key)
            with open(audio_file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=audio_file
                )
            return transcription.text
        elif model == 'deepgram':
            # Placeholder for Deepgram STT model transcription
            pass
            # client = Deepgram(api_key=api_key)
            # with open(audio_file_path, "rb") as audio_file:
            #     transcription = client.transcription.pre_recorded(audio_file, {'punctuate': True, 'model': "whisper"})
            # return transcription['results']['channels'][0]['alternatives'][0]['transcript']
        elif model == 'local':
            # Placeholder for local STT model transcription
            return "Transcribed text from local model"
        else:
            raise ValueError("Unsupported transcription model")
    except Exception as e:
        logging.error(f"Failed to transcribe audio: {e}")
        return "Error in transcribing audio"
