# VERBI - Voice Assistant 🎙️

## Motivation ✨✨✨

Welcome to the Voice Assistant project! 🎙️ Our goal is to create a modular voice assistant application that allows you to experiment with state-of-the-art (SOTA) models for various components. The modular structure provides flexibility, enabling you to pick and choose between different SOTA models for transcription, response generation, and text-to-speech (TTS). This approach facilitates easy testing and comparison of different models, making it an ideal platform for research and development in voice assistant technologies. Whether you're a developer, researcher, or enthusiast, this project is for you!

## Features 🧰

- **Modular Design**: Easily switch between different models for transcription, response generation, and TTS.
- **Support for Multiple APIs**: Integrates with OpenAI, Groq, and Deepgram APIs, along with placeholders for local models.
- **Audio Recording and Playback**: Record audio from the microphone and play generated speech.
- **Configuration Management**: Centralized configuration in `config.py` for easy setup and management.

## Project Structure 📂

```plaintext
voice_assistant/
├── voice_assistant/
│   ├── __init__.py
│   ├── audio.py
│   ├── api_key_manager.py
│   ├── config.py
│   ├── transcription.py
│   ├── response_generation.py
│   ├── text_to_speech.py
│   ├── utils.py
├── .env
├── run_voice_assistant.py
├── setup.py
├── requirements.txt
└── README.md
```

## Setup Instructions  📋

#### Prerequisites ✅

- Python 3.10 or higher
- Virtual environment (recommended)

#### Step-by-Step Instructions 🔢

1. 📥 **Clone the repository**

```shell
   git clone https://github.com/PromtEngineer/Verbi.git
   cd Verbi
```
2. 🐍 **Set up a virtual environment**

  Using `venv`:

```shell
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
  Using `conda`:

```shell
    conda create --name verbi python=3.10
    conda activate verbi
```
3.  📦 **Install the required packages**

```shell
   pip install -r requirements.txt
```
4. 🛠️ **Set up the environment variables**

Create a  `.env` file in the root directory and add your API keys:
```shell
    OPENAI_API_KEY=your_openai_api_key
    GROQ_API_KEY=your_groq_api_key
    DEEPGRAM_API_KEY=your_deepgram_api_key
    LOCAL_MODEL_PATH=path/to/local/model
```
4. 🧩 **Configure the models**

Edit config.py to select the models you want to use:

```shell
    class Config:
        # Model selection
        TRANSCRIPTION_MODEL = 'groq'  # Options: 'openai', 'groq', 'deepgram', 'local'
        RESPONSE_MODEL = 'groq'       # Options: 'openai', 'groq', 'local'
        TTS_MODEL = 'deepgram'        # Options: 'openai', 'deepgram', 'local'

        # API keys and paths
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
        LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH")
```
4.  🏃 **Run the voice assistant**

```shell
   python run_voice_assistant.py
```
## Model Options ⚙️

#### Transcription Models  🎤

- **OpenAI**: Uses OpenAI's Whisper model.
- **Groq**: Uses Groq's Whisper-large-v3 model.
- **Deepgram**: Placeholder for Deepgram's transcription model.
- **Local**: Placeholder for a local speech-to-text (STT) model.

#### Response Generation Models  💬

- **OpenAI**: Uses OpenAI's GPT-4 model.
- **Groq**: Uses Groq's LLaMA model.
- **Local**: Placeholder for a local language model.

#### Text-to-Speech (TTS) Models  🔊

- **OpenAI**: Uses OpenAI's TTS model with the "fable" voice.
- **Deepgram**: Uses Deepgram's TTS model with the "aura-angus-en" voice.
- **Local**: Placeholder for a local TTS model.

## Detailed Module Descriptions  📘

- **`run_verbi.py`**: Main script to run the voice assistant.
- **`voice_assistant/config.py`**: Manages configuration settings and API keys.
- **`voice_assistant/api_key_manager.py`**: Handles retrieval of API keys based on configured models.
- **`voice_assistant/audio.py`**: Functions for recording and playing audio.
- **`voice_assistant/transcription.py`**: Manages audio transcription using various APIs.
- **`voice_assistant/response_generation.py`**: Handles generating responses using various language models.
- **`voice_assistant/text_to_speech.py`**: Manages converting text responses into speech.
- **`voice_assistant/utils.py`**: Contains utility functions like deleting files.
- **`voice_assistant/__init__.py`**: Initializes the `voice_assistant` package.

## Roadmap 🛤️🛤️🛤️

Here's what's next for the Voice Assistant project:

1. **Add Support for Streaming**: Enable real-time streaming of audio input and output.
2. **Add Support for ElevenLabs and Enhanced Deepgram for TTS**: Integrate additional TTS options for higher quality and variety.
3. **Add Filler Audios**: Include background or filler audios while waiting for model responses to enhance user experience.
4. **Add Support for Local Models Across the Board**: Expand support for local models in transcription, response generation, and TTS.

## Contributing 🤝

We welcome contributions from the community! If you'd like to help improve this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request detailing your changes.



