import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Dict, Any
import pytest
from unittest.mock import Mock, MagicMock


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def temp_file(temp_dir: Path) -> Generator[Path, None, None]:
    """Create a temporary file within the temporary directory."""
    temp_file_path = temp_dir / "test_file.txt"
    temp_file_path.write_text("Test content")
    yield temp_file_path


@pytest.fixture
def mock_config() -> Dict[str, Any]:
    """Provide a mock configuration dictionary."""
    return {
        "api_key": "test-api-key",
        "model": "test-model",
        "temperature": 0.7,
        "max_tokens": 100,
        "debug": True,
        "log_level": "DEBUG",
        "timeout": 30,
    }


@pytest.fixture
def mock_env_vars(monkeypatch) -> Dict[str, str]:
    """Set up mock environment variables."""
    env_vars = {
        "OPENAI_API_KEY": "test-openai-key",
        "GROQ_API_KEY": "test-groq-key",
        "DEEPGRAM_API_KEY": "test-deepgram-key",
        "ELEVENLABS_API_KEY": "test-elevenlabs-key",
        "DEBUG": "true",
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars


@pytest.fixture
def mock_api_response() -> Dict[str, Any]:
    """Provide a mock API response structure."""
    return {
        "id": "test-response-id",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "test-model",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Test response content"
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }


@pytest.fixture
def mock_audio_data() -> bytes:
    """Provide mock audio data for testing."""
    return b'\x00\x01' * 1000


@pytest.fixture
def mock_llm_client():
    """Create a mock LLM client."""
    client = Mock()
    client.generate_response = MagicMock(return_value="Test LLM response")
    client.is_connected = MagicMock(return_value=True)
    return client


@pytest.fixture
def mock_tts_client():
    """Create a mock TTS client."""
    client = Mock()
    client.synthesize = MagicMock(return_value=b'\x00\x01' * 1000)
    client.is_available = MagicMock(return_value=True)
    return client


@pytest.fixture
def mock_stt_client():
    """Create a mock STT client."""
    client = Mock()
    client.transcribe = MagicMock(return_value="Test transcription")
    client.is_available = MagicMock(return_value=True)
    return client


@pytest.fixture(autouse=True)
def reset_singleton_instances():
    """Reset any singleton instances between tests."""
    yield


@pytest.fixture
def capture_logs(caplog):
    """Capture log messages during tests."""
    with caplog.at_level("DEBUG"):
        yield caplog


@pytest.fixture
def mock_file_system(tmp_path):
    """Create a mock file system structure for testing."""
    dirs = ["config", "data", "logs", "models"]
    for dir_name in dirs:
        (tmp_path / dir_name).mkdir()
    
    config_file = tmp_path / "config" / "config.json"
    config_file.write_text('{"test": true}')
    
    return tmp_path


@pytest.fixture
def performance_timer():
    """Measure test performance."""
    import time
    start_time = time.time()
    yield
    end_time = time.time()
    print(f"\nTest execution time: {end_time - start_time:.3f} seconds")


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Provide path to test data directory."""
    return Path(__file__).parent / "test_data"


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Mark test as a unit test")
    config.addinivalue_line("markers", "integration: Mark test as an integration test")
    config.addinivalue_line("markers", "slow: Mark test as slow running")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)