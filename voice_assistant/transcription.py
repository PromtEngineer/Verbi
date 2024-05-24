# voice_assistant/transcription.py
from colorama import Fore, init
from openai import OpenAI
from groq import Groq
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
import json
import logging
import requests
import time

fast_url = "http://localhost:8000"
checked_fastwhisperapi = False

def check_fastwhisperapi():
    global checked_fastwhisperapi
    global fast_url
    if not checked_fastwhisperapi:
        infopoint = fast_url + "/info"
        try:
            response = requests.get(infopoint)
            if response.status_code != 200:
                raise Exception("FastWhisperAPI is not running")
        except Exception:
            raise Exception("FastWhisperAPI is not running")
        checked_fastwhisperapi = True
def transcribe_audio(model, api_key, audio_file_path, local_model_path=None):
    """
    Transcribe an audio file using the specified model.
    
    Args:
    model (str): The model to use for transcription ('openai', 'groq', 'deepgram', 'fastwhisper', 'local').
    api_key (str): The API key for the transcription service.
    audio_file_path (str): The path to the audio file to transcribe.
    local_model_path (str): The path to the local model (if applicable).

    Returns:
    str: The transcribed text.
    """
    # measure the transcription response time
    # start_time = time.time()
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
        
        elif model == 'fastwhisperapi':
            global fast_url
            check_fastwhisperapi()

            endpoint = fast_url + "/v1/transcriptions"

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
                
            }
            response = requests.post(endpoint, files=files, data=data, headers=headers)
            response_json = response.json()
            return response_json.get('text', 'No text found in the response.')
          
        elif model == 'local':
            # Placeholder for local STT model transcription
            return "Transcribed text from local model"
        else:
            raise ValueError("Unsupported transcription model")

    except Exception as e:
        logging.error(Fore.RED + f"Failed to transcribe audio: {e}" + Fore.RESET)
        raise Exception("Error in transcribing audio")
    # finally:
    #     # end the transcription response time
    #     time_difference = time.time() - start_time
    #     logging.info(Fore.YELLOW + f"Time taken to transcribe: {time_difference} seconds" + Fore.RESET)
