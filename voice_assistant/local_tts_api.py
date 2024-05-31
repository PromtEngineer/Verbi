from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from melo.api import TTS
from config import Config
import torch
import uuid

app = FastAPI()

class TextToSpeechRequest(BaseModel):
    """
    Model representing a text-to-speech request.
    
    Attributes:
        text (str): The text to convert to speech.
        language (str): The language of the text.
        accent (str): The accent to use for the speech.
        speed (float): The speed of the speech.
        filename (str): The desired name for the output audio file.
    """
    text: str
    language: str = 'EN'
    accent: str = 'EN-US'
    speed: float = 1.0
    filename: str = Field(default_factory=lambda: f"{uuid.uuid4()}.wav")

def get_device():
    """
    Determine the appropriate device for running the TTS model.
    
    Returns:
        str: The device to use ('cuda', 'mps', or 'cpu').
    """
    if torch.cuda.is_available():
        return 'cuda'
    elif torch.backends.mps.is_available():
        return 'mps'
    else:
        return 'cpu'

# Initialize the TTS model
device = get_device()  # Determine the appropriate device
model = TTS(language='EN', device=device)
speaker_ids = model.hps.data.spk2id


@app.post("/generate-audio/")
def generate_audio(request: TextToSpeechRequest):
    """
    Generate an audio file from the given text.

    Args:
        request (TextToSpeechRequest): The request containing text and other parameters.

    Returns:
        dict: A dictionary containing a message and the file path of the generated audio.
    
    Raises:
        HTTPException: If the specified accent is invalid or if there is an error during audio generation.
    """
    if request.accent not in speaker_ids:
        raise HTTPException(status_code=400, detail="Invalid accent specified")
    
    try:
        # Use the provided filename or generate a unique one
        output_filename = request.filename
        
        # Generate the audio file
        model.tts_to_file(request.text, speaker_ids[request.accent], output_filename, speed=request.speed)
        
        return {"message": "Audio file generated successfully", "file_path": output_filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=Config.TTS_PORT_LOCAL)