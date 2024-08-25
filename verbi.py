import streamlit as st
from voice_assistant.audio import play_audio, record_audio
from voice_assistant.transcription import transcribe_audio
from voice_assistant.response_generation import generate_response
from voice_assistant.text_to_speech import text_to_speech
from voice_assistant.utils import delete_file
from voice_assistant.api_key_manager import get_transcription_api_key, get_response_api_key, get_tts_api_key
from voice_assistant.config import Config
import time
import base64

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def main():
    st.title('Voice to Voice AI Assistant')

    # Button to start the conversation
    if st.button('Start Talking'):
        with st.spinner('Listening...'):
            record_audio(Config.INPUT_AUDIO)
            transcription_api_key = get_transcription_api_key()
            user_input = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.INPUT_AUDIO, Config.LOCAL_MODEL_PATH)

            if not user_input:
                st.error("No audio detected. Please try again.")
                return

            st.write('You said:', user_input)
            response_api_key = get_response_api_key()
            chat_history = [{"role": "user", "content": user_input}]
            response_text = generate_response(Config.RESPONSE_MODEL, response_api_key, chat_history, Config.LOCAL_MODEL_PATH)
            st.write('AI Response:', response_text)

            tts_api_key = get_tts_api_key()
            output_file = 'output.mp3' if Config.TTS_MODEL in ['openai', 'elevenlabs', 'melotts', 'cartesia'] else 'output.wav'
            text_to_speech(Config.TTS_MODEL, tts_api_key, response_text, output_file, Config.LOCAL_MODEL_PATH)

            # Automatically play audio response
            autoplay_audio(output_file)

            # Cleanup
            delete_file(Config.INPUT_AUDIO)
            delete_file(output_file)

if __name__ == "__main__":
    main()