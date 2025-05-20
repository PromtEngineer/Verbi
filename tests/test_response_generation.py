import unittest
from unittest.mock import patch, MagicMock

from voice_assistant.response_generation import _generate_gemini_response
from voice_assistant.config import Config

class TestGeminiResponseGeneration(unittest.TestCase):

    @patch('voice_assistant.response_generation.genai.Client')
    @patch('voice_assistant.response_generation.Config')
    def test_generate_gemini_response_success(self, MockConfig, MockGeminiClient):
        # Configure mock Config values
        MockConfig.GEMINI_API_KEY = "test_api_key"
        MockConfig.GEMINI_MODEL = "test_gemini_model"

        # Setup mock Gemini client and methods
        mock_client_instance = MockGeminiClient.return_value
        mock_chat_instance = MagicMock()
        mock_client_instance.chats.create.return_value = mock_chat_instance
        
        mock_response = MagicMock()
        mock_response.text = "Mocked Gemini response"
        mock_chat_instance.send_message.return_value = mock_response

        # Sample chat history
        chat_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "How are you?"}
        ]

        # Call the function
        response_text = _generate_gemini_response(chat_history)

        # Assertions
        MockGeminiClient.assert_called_once_with(api_key="test_api_key")
        
        expected_gemini_history = [
            {"role": "user", "parts": [{"text": "Hello"}]},
            {"role": "model", "parts": [{"text": "Hi there!"}]},
        ]
        mock_client_instance.chats.create.assert_called_once_with(
            model="test_gemini_model",
            history=expected_gemini_history
        )
        
        mock_chat_instance.send_message.assert_called_once_with("How are you?")
        self.assertEqual(response_text, "Mocked Gemini response")

    @patch('voice_assistant.response_generation.genai.Client')
    @patch('voice_assistant.response_generation.Config')
    def test_generate_gemini_response_api_error(self, MockConfig, MockGeminiClient):
        # Configure mock Config values
        MockConfig.GEMINI_API_KEY = "test_api_key"
        MockConfig.GEMINI_MODEL = "test_gemini_model"

        # Setup mock Gemini client to raise an exception
        MockGeminiClient.side_effect = Exception("API Error")

        # Sample chat history
        chat_history = [
            {"role": "user", "content": "Hello"}
        ]

        # Call the function
        response_text = _generate_gemini_response(chat_history)

        # Assertions
        MockGeminiClient.assert_called_once_with(api_key="test_api_key")
        self.assertEqual(response_text, "I'm sorry, I couldn't generate a response at the moment.")

    @patch('voice_assistant.response_generation.genai.Client')
    @patch('voice_assistant.response_generation.Config')
    def test_generate_gemini_response_empty_history(self, MockConfig, MockGeminiClient):
        # Configure mock Config values
        MockConfig.GEMINI_API_KEY = "test_api_key"
        MockConfig.GEMINI_MODEL = "test_gemini_model"
        
        # Sample chat history
        chat_history = []

        # Call the function
        response_text = _generate_gemini_response(chat_history)
        
        # This will fail because the function tries to access chat_history[-1]
        # which will raise an IndexError for an empty list.
        # The function should ideally handle this, but for now, testing existing behavior.
        self.assertEqual(response_text, "I'm sorry, I couldn't generate a response at the moment.")


if __name__ == '__main__':
    unittest.main()
