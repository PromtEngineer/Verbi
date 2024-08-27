# voice_assistant/response_generation.py

from openai import OpenAI
from groq import Groq
import ollama
import logging
import google.generativeai as genai
from voice_assistant.config import Config


def generate_response(model, api_key, chat_history, local_model_path=None):
    """
    Generate a response using the specified model.
    
    Args:
    model (str): The model to use for response generation ('openai', 'groq', 'local').
    api_key (str): The API key for the response generation service.
    chat_history (list): The chat history as a list of messages.
    local_model_path (str): The path to the local model (if applicable).

    Returns:
    str: The generated response text.
    """
    try:
        if model == 'openai':
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=Config.OPENAI_LLM,
                messages=chat_history
            )
            return response.choices[0].message.content
        elif model == 'groq':
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model=Config.GROQ_LLM, #"llama3-8b-8192",
                messages=chat_history
            )
            return response.choices[0].message.content
        elif model == 'ollama':
            response = ollama.chat(
                model=Config.OLLAMA_LLM,
                messages=chat_history,
                # stream=True,
            )
            return response['message']['content']
        elif model == 'gemini':
            genai.configure(api_key=Config.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Convert chat history to the required format
            # The current chat history structure is not compatible with the gemini model
            # It expects the chat history to be in the format [{"role": "model", "parts": ""}] and [{"role": "user", "parts": ""}]
            # However, the current chat history is in the format [{"role": "system", "content": ""}] and [{"role": "user", "content": ""}]
            # To make it compatible, we need to convert the chat history by replacing "content" with "parts"
            # Iterate over each message in the chat history
            converted_chat_history = [
                {"role": "model" if message["role"] == "system" else message["role"], "parts": message["content"]}
                for message in chat_history
            ]
            # Extract and remove the last user message
            user_text = ""
            for message in reversed(converted_chat_history):
                if message["role"] == "user":
                    converted_chat_history.remove(message)
                    user_text = message["parts"]
                    break
            # Start a new chat and generate a response
            chat = model.start_chat(
                history=converted_chat_history
            )
            response = chat.send_message(user_text)
            return response.text
        elif model == 'local':
            # Placeholder for local LLM response generation
            return "Generated response from local model"
        else:
            raise ValueError("Unsupported response generation model")
    except Exception as e:
        logging.error(f"Failed to generate response: {e}")
        return "Error in generating response"
