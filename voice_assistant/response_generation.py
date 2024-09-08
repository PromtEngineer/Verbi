# voice_assistant/response_generation.py

import logging
import google.generativeai as genai

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
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel(Config.GEMINI_MODEL)
        chat = model.start_chat(history=[])
        
        for message in chat_history:
            if message['role'] == 'user':
                chat.send_message(message['content'])
            elif message['role'] == 'assistant':
                # Simulate assistant messages in the chat history
                chat.history.append({"role": "model", "parts": [message['content']]})
        
        response = chat.send_message(chat_history[-1]['content'])
        return response.text
    except Exception as e:
        logging.error(f"Error generating Gemini response: {e}")
        return "I'm sorry, I couldn't generate a response at the moment."