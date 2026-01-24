# voice_assistant/text_to_speech.py
import logging
import json
import pyaudio
import elevenlabs
import soundfile as sf
import requests
import wave
from google import genai
from google.genai import types

from openai import OpenAI
from deepgram import DeepgramClient
from elevenlabs.client import ElevenLabs
from cartesia import Cartesia

from voice_assistant.config import Config
from voice_assistant.local_tts_generation import generate_audio_file_melotts

def text_to_speech(model: str, api_key:str, text:str, output_file_path:str, local_model_path:str=None):
    """
    Convert text to speech using the specified model.
    
    Args:
    model (str): The model to use for TTS ('openai', 'deepgram', 'elevenlabs', 'local').
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
                voice="nova",
                input=text
            )

            speech_response.stream_to_file(output_file_path)
            # with open(output_file_path, "wb") as audio_file:
            #     audio_file.write(speech_response['data'])  # Ensure this correctly accesses the binary content

        elif model == 'deepgram':
            client = DeepgramClient(api_key=api_key)
            response = client.speak.v1.audio.generate(
                text=text,
                model="aura-arcas-en",  # https://developers.deepgram.com/docs/tts-models
            )
            
            # Save the audio file
            with open(output_file_path, "wb") as audio_file:
                audio_file.write(response.stream.getvalue())
        
        elif model == 'elevenlabs':
            client = ElevenLabs(api_key=api_key)
            audio = client.generate(
                text=text, 
                voice="Paul J.", 
                output_format="mp3_22050_32", 
                model="eleven_turbo_v2"
            )
            elevenlabs.save(audio, output_file_path)

        elif model == 'gemini':
            client = genai.Client(api_key=api_key)
            
            response = client.models.generate_content(
                model=Config.GEMINI_TTS_MODEL,
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=Config.GEMINI_TTS_VOICE
                            )
                        )
                    )
                )
            )
            
            # Get PCM audio data and save as proper WAV file with headers
            audio_data = response.candidates[0].content.parts[0].inline_data.data
            
            # Write as WAV file with proper headers (24kHz, 16-bit, mono)
            with wave.open(output_file_path, "wb") as wf:
                wf.setnchannels(1)  # mono
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(24000)  # 24kHz sample rate
                wf.writeframes(audio_data)
        
        elif model == "cartesia":
            client = Cartesia(api_key=api_key)
            # voice_name = "Barbershop Man"
            voice_id = "f114a467-c40a-4db8-964d-aaba89cd08fa"#"a0e99841-438c-4a64-b679-ae501e7d6091"
            voice = client.voices.get(id=voice_id)

            # You can check out our models at https://docs.cartesia.ai/getting-started/available-models
            model_id = "sonic-english"

            # You can find the supported `output_format`s at https://docs.cartesia.ai/api-reference/endpoints/stream-speech-server-sent-events
            output_format = {
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            }

            p = pyaudio.PyAudio()
            rate = 44100

            stream = None

            # Generate and stream audio
            for output in client.tts.sse(
                model_id=model_id,
                transcript=text,
                voice_embedding=voice["embedding"],
                stream=True,
                output_format=output_format,
            ):
                buffer = output["audio"]

                if stream is None:
                    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=rate, output=True)

                # Write the audio data to the stream
                stream.write(buffer)
            
            if stream:
                stream.stop_stream()
                stream.close()
            p.terminate()

        elif model == "melotts": # this is a local model
            generate_audio_file_melotts(text=text, filename=output_file_path)

        elif model == "piper":  # this is a local model
            try:
                response = requests.post(
                    f"{Config.PIPER_SERVER_URL}/synthesize/",
                    json={"text": text},
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    with open(Config.PIPER_OUTPUT_FILE, "wb") as f:
                        f.write(response.content)
                    logging.info(f"Piper TTS output saved to {Config.PIPER_OUTPUT_FILE}")
                else:
                    logging.error(f"Piper TTS API error: {response.status_code} - {response.text}")

            except Exception as e:
                logging.error(f"Piper TTS request failed: {e}")
        
        elif model == 'local':
            with open(output_file_path, "wb") as f:
                f.write(b"Local TTS audio data")
        
        else:
            raise ValueError("Unsupported TTS model")
        
    except Exception as e:
        logging.error(f"Failed to convert text to speech: {e}")