# voice_assistant/response_generation.py

from openai import OpenAI
from groq import Groq
import ollama
import logging
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
        elif model == 'local':
            # Placeholder for local LLM response generation
            return "Generated response from local model"
        else:
            raise ValueError("Unsupported response generation model")
    except Exception as e:
        logging.error(f"Failed to generate response: {e}")
        return "Error in generating response"
