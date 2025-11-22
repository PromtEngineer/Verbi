# voice_assistant/response_generation.py

import logging

from openai import OpenAI
from groq import Groq
import ollama
import anthropic
import google.generativeai as genai

from voice_assistant.config import Config


def generate_response(model:str, api_key:str, chat_history:list, local_model_path:str=None):
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
            return _generate_openai_response(api_key, chat_history)
        elif model == 'groq':
            return _generate_groq_response(api_key, chat_history)
        elif model == 'ollama':
            return _generate_ollama_response(chat_history)
        elif model == 'anthropic':
            return _generate_anthropic_response(api_key, chat_history)
        elif model == 'google':
            return _generate_google_response(api_key, chat_history)
        elif model == 'local':
            # Placeholder for local LLM response generation
            return "Generated response from local model"
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

def _generate_anthropic_response(api_key, chat_history):
    client = anthropic.Anthropic(api_key=api_key)
    # Convert chat_history to Anthropic format if needed
    # Anthropic expects: [{"role": "user", "content": "..."}] or [{"role": "assistant", "content": "..."}]
    # System message is passed separately in `system` parameter.

    system_prompt = ""
    messages = []
    for msg in chat_history:
        if msg['role'] == 'system':
            system_prompt = msg['content']
        else:
            messages.append(msg)

    message = client.messages.create(
        model=Config.ANTHROPIC_LLM,
        max_tokens=1024,
        system=system_prompt,
        messages=messages
    )
    return message.content[0].text

def _generate_google_response(api_key, chat_history):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(Config.GOOGLE_LLM)

    # Google Generative AI (Gemini) chat history format:
    # history = [
    #   {"role": "user", "parts": "Hello"},
    #   {"role": "model", "parts": "Great to meet you. What would you like to know?"}
    # ]
    # Note: 'system' role is supported via system_instruction in model creation,
    # but for simplicity here we might prepend it to the first message or just use the chat structure.
    # Gemini 1.5 supports system instructions.

    system_instruction = None
    history = []

    last_message = chat_history[-1]['content']

    # Prepare history excluding the last message which is the new prompt
    # Also handle system prompt

    for msg in chat_history[:-1]:
        if msg['role'] == 'system':
            system_instruction = msg['content']
        elif msg['role'] == 'user':
            history.append({"role": "user", "parts": msg['content']})
        elif msg['role'] == 'assistant':
            history.append({"role": "model", "parts": msg['content']})

    # Re-initialize model with system instruction if present
    if system_instruction:
        model = genai.GenerativeModel(Config.GOOGLE_LLM, system_instruction=system_instruction)

    chat = model.start_chat(history=history)
    response = chat.send_message(last_message)
    return response.text