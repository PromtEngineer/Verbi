# voice_assistant/transcription.py

from openai import OpenAI
from groq import Groq
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
import json
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
            try:
                # STEP 1 Create a Deepgram client using the API key
                deepgram = DeepgramClient(api_key)

                with open(audio_file_path, "rb") as file:
                    buffer_data = file.read()

                payload: FileSource = {
                    "buffer": buffer_data,
                }

                #STEP 2: Configure Deepgram options for audio analysis
                options = PrerecordedOptions(
                    model="nova-2",
                    smart_format=True,
                )
 
                # STEP 3: Call the transcribe_file method with the text payload and options
                response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

                # STEP 4: Print and parse the response
                response_json = response.to_json()

                # Parse the JSON string into a Python dictionary
                data = json.loads(response_json)

                # Extract and print the transcript
                transcript = data['results']['channels'][0]['alternatives'][0]['transcript']

                # Return the transcript
                return transcript

            except Exception as e:
                print(f"Exception: {e}")
                
        elif model == 'local':
            # Placeholder for local STT model transcription
            return "Transcribed text from local model"
        else:
            raise ValueError("Unsupported transcription model")
    except Exception as e:
        logging.error(f"Failed to transcribe audio: {e}")
        return "Error in transcribing audio"
