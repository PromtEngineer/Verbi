# voice_assistant/transcription.py

from openai import OpenAI
from groq import Groq
from deepgram import Deepgram
import logging
import requests

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
                    file=audio_file,

                    # Add language model parameter to improve transcription accuracy
                    language='en'
                )
            return transcription.text
        elif model == 'groq':
            client = Groq(api_key=api_key)
            with open(audio_file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=audio_file,
                    # Add language model parameter to improve transcription accuracy
                    language='en'
                )
            return transcription.text
        elif model == 'deepgram':
            # Placeholder for Deepgram STT model transcription
            pass
            # client = Deepgram(api_key=api_key)
            # with open(audio_file_path, "rb") as audio_file:
            #     transcription = client.transcription.pre_recorded(audio_file, {'punctuate': True, 'model': "whisper"})
            # return transcription['results']['channels'][0]['alternatives'][0]['transcript']
        elif model == 'fastwhisperapi':
            url = "http://localhost:8000/v1/transcriptions"
        
            files = {
                'file': (audio_file_path, open(audio_file_path, 'rb')),
            }
            data = {
                'model': "base", # possible values: tiny, base, small, medium, large
                'language': "en", # possible values language ISO codes. Set None for auto detection
                'initial_prompt': None, # optional initial prompt for the model useful for context and spelling
                'vad_filter': True, # set to True to avoid model transcription allucinations on silence
            }
            headers = {
                'Authorization': 'Bearer dummy_api_key',
                'Contetnt-Type': 'multipart/form-data'
            }
            
            response = requests.post(url, files=files, data=data, headers=headers)
            response_json = response.json()
            return response_json.get('text', 'No text found in the response.')
        elif model == 'local':
            # Placeholder for local STT model transcription
            return "Transcribed text from local model"
        else:
            raise ValueError("Unsupported transcription model")
    except Exception as e:
        logging.error(f"Failed to transcribe audio: {e}")
        return "Error in transcribing audio"
