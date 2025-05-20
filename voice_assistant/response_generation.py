# voice_assistant/response_generation.py

import logging
from google import genai

from openai import OpenAI
from groq import Groq
import ollama
from cerebras.cloud.sdk import Cerebras
from voice_assistant.config import Config


def generate_response(model:str, api_key:str, chat_history:list, local_model_path:str=None):
    """
    Generate a response using the specified model.
    
    Args:
    model (str): The model to use for response generation ('openai', 'groq', 'ollama', 'cerebras', 'gemini', 'local').
    api_key (str): The API key for the response generation service.
    chat_history (list): The chat history as a list of messages.
    local_model_path (str): The path to the local model (if applicable).

    Returns:
    str: The generated response text.
    """
    try:
        if model == 'openai':
            return _generate_openai_response(api_key, chat_history)
        elif model == 'groq':
            return _generate_groq_response(api_key, chat_history)
        elif model == 'ollama':
            return _generate_ollama_response(chat_history)
        elif model == 'local':
            # Placeholder for local LLM response generation
            return "Generated response from local model"
        elif model == 'cerebras':
            return _generate_cerebras_response(chat_history)
        elif model == 'gemini':
            return _generate_gemini_response(chat_history)
        else:
            raise ValueError("Unsupported response generation model")
    except Exception as e:
        logging.error(f"Failed to generate response: {e}")
        return "Error in generating response"

def _generate_openai_response(api_key, chat_history):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=Config.OPENAI_LLM,
        messages=chat_history
    )
    return response.choices[0].message.content


def _generate_groq_response(api_key, chat_history):
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=Config.GROQ_LLM,
        messages=chat_history
    )
    return response.choices[0].message.content


def _generate_ollama_response(chat_history):
    response = ollama.chat(
        model=Config.OLLAMA_LLM,
        messages=chat_history,
    )
    return response['message']['content']


def _generate_cerebras_response(chat_history):
    try:
        cerebras_client = Cerebras(api_key=Config.CEREBRAS_API_KEY)
        chat_completion = cerebras_client.chat.completions.create(
            messages=chat_history,
            model=Config.CEREBRAS_MODEL,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating Cerebras response: {e}")
        return "I'm sorry, I couldn't generate a response at the moment."


def _generate_gemini_response(chat_history):
    try:
        client = genai.Client(api_key=Config.GEMINI_API_KEY)
        
        # Convert chat_history to the format expected by the new SDK
        gemini_history = []
        for message in chat_history[:-1]: # Exclude the last message, it will be sent separately
            role = "user" if message['role'] == 'user' else "model"
            gemini_history.append({
                "role": role,
                "parts": [{"text": message['content']}]
            })

        chat = client.chats.create(model=Config.GEMINI_MODEL, history=gemini_history)
        
        # Send the last user message
        last_message_content = chat_history[-1]['content']
        response = chat.send_message(last_message_content)
        return response.text
    except Exception as e:
        logging.error(f"Error generating Gemini response: {e}")
        return "I'm sorry, I couldn't generate a response at the moment."