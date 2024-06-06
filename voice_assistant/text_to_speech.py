# voice_assistant/text_to_speech.py
import logging
import requests

from openai import OpenAI
from deepgram import DeepgramClient, SpeakOptions
from cartesia.tts import CartesiaTTS
from voice_assistant.audio import play_audio_stream
import soundfile as sf
import json


from voice_assistant.local_tts_generation import generate_audio_file_melotts

def text_to_speech(model, api_key, text, output_file_path, local_model_path=None):
    """
    Convert text to speech using the specified model.
    
    Args:
    model (str): The model to use for TTS ('openai', 'deepgram', 'elevenlabs', 'cartesia', 'melotts', 'fastxttsapi', 'local').
    api_key (str): The API key for the TTS service.
    text (str): The text to convert to speech.
    output_file_path (str): The path to save the generated speech audio file.
    local_model_path (str): The path to the local model (if applicable).
    """
    
    try:
        if model == 'openai':
            client = OpenAI(api_key=api_key)
            speech_response = client.audio.speech.create(
                model="tts-1",
                voice="fable",
                input=text
            )

            speech_response.stream_to_file(output_file_path)
            # with open(output_file_path, "wb") as audio_file:
            #     audio_file.write(speech_response['data'])  # Ensure this correctly accesses the binary content

        elif model == 'deepgram':
            client = DeepgramClient(api_key=api_key)
            options = SpeakOptions(
                model="aura-luna-en", # Change voice if needed
                encoding="linear16",
                container="wav"
            )
            SPEAK_OPTIONS = {"text": text}
            response = client.speak.v("1").save(output_file_path, SPEAK_OPTIONS, options)
        elif model == 'elevenlabs':
            ELEVENLABS_VOICE_ID = "Paul J."
            ELEVENLABS_URL = f'https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}/stream'
            headers = {
                'accept': '*/*',
                'xi-api-key': api_key,
                'Content-Type': 'application/json'
            }
            data = {
                'text': text,
                'voice_settings': {
                    'stability': 0.50,
                    'similarity_boost': 0.75
                },
                "output_format": "mp3_22050_32" 
            }
        
            with requests.post(ELEVENLABS_URL, headers=headers, json=data, stream=True) as r:
                audio_stream = r.iter_content(chunk_size=512)
                play_audio_stream(audio_stream)
        elif model == "cartesia":
            # config
            with open('Barbershop Man.json') as f:
                voices = json.load(f)

            # voice_id = voices["Barbershop Man"]["id"]
            voice = voices["Barbershop Man"]["embedding"]
            gen_cfg = dict(model_id="upbeat-moon", data_rtype='array', output_format='fp32')

            # create client
            client = CartesiaTTS(api_key=api_key)

            # generate audio
            output = client.generate(transcript=text, voice=voice, stream=False, **gen_cfg)

            # save audio to file
            buffer = output["audio"]
            rate = output["sampling_rate"]
            sf.write(output_file_path, buffer, rate) 

        elif model == "melotts": # this is a local model
            generate_audio_file_melotts(text=text, filename=output_file_path)
        elif model == "fastxttsapi":
            # Set the URL for the FastXTTS API, change with the address of where the API is running either locally or on a server
            FASTXTTSAPI_URL = 'https://localhost:8000'
            payload = {
                "text": text,
                "language": "en",  
                "voice": "Dionisio Schuyler",  #Query the endpoint https://localhost:8000/voices to get the list of available voices
                "stream": True,
            }
            with requests.post(FASTXTTSAPI_URL + "/v1/speech", json=payload, verify=False) as r:
                audio_stream = r.iter_content(chunk_size=512)
                play_audio_stream(audio_stream)
        elif model == 'local':
            # Placeholder for local TTS model
            with open(output_file_path, "wb") as f:
                f.write(b"Local TTS audio data")
        else:
            raise ValueError("Unsupported TTS model")
    except Exception as e:
        logging.error(f"Failed to convert text to speech: {e}")
