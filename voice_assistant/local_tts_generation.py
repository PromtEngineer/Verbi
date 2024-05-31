import requests
from voice_assistant.config import Config


def generate_audio_file_melotts(text, language='EN', accent='EN-US', speed=1.0, filename=None):
    """
    Generate an audio file from the given text using the FastAPI endpoint.

    Args:
        text (str): The text to convert to speech.
        language (str): The language of the text. Default is 'EN'.
        accent (str): The accent to use for the speech. Default is 'EN-US'.
        speed (float): The speed of the speech. Default is 1.0.
        filename (str, optional): The desired name for the output audio file. If None, a unique name will be generated.

    Returns:
        dict: A dictionary containing the message and the file path of the generated audio.
    """
    # Define the API endpoint
    url = f"http://localhost:{Config.TTS_PORT_LOCAL}/generate-audio/"

    # Define the payload
    payload = {
        "text": text,
        "language": language,
        "accent": accent,
        "speed": speed
    }

    if filename:
        payload["filename"] = filename

    # Set the headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the POST request
    response = requests.post(url, json=payload, headers=headers)

    # Check the response
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Example usage of the function
if __name__ == "__main__":
    try:
        result = generate_audio_file_melotts(
            text="What is the purpose of life?",
            language="EN",
            accent="EN-US",
            speed=1.0,
            filename="my_custom_audio.wav"
        )
        print("Audio file generated successfully")
        print("File path:", result.get("file_path"))
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")