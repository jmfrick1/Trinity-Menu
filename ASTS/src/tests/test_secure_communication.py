import unittest
from unittest.mock import patch, MagicMock
from src.utilities import secure_api_request, encrypt_message, decrypt_message

class TestSecureCommunication(unittest.TestCase):

    def setUp(self):
        # Setup any necessary resources or initializations
        pass

    def tearDown(self):
        # Clean up after each test if necessary
        pass

    @patch('src.utilities.requests.post')
    def test_secure_api_request_success(self, mock_requests_post):
        # Mocking the requests.post function
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'ok'}
        mock_requests_post.return_value = mock_response

        # Call the function under test
        response = secure_api_request("test-endpoint", {"param": "value"})

        # Assertions
        mock_requests_post.assert_called_once_with('https://api.example.com/test-endpoint', json={'param': 'value'})
        self.assertEqual(response, {'status': 'ok'})

    @patch('src.utilities.requests.post')
    def test_secure_api_request_failure(self, mock_requests_post):
        # Mocking the requests.post function to simulate a failure
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'error'}
        mock_requests_post.return_value = mock_response

        # Call the function under test
        response = secure_api_request("test-endpoint", {"param": "value"})

        # Assertions
        mock_requests_post.assert_called_once_with('https://api.example.com/test-endpoint', json={'param': 'value'})
        self.assertEqual(response, {'status': 'error'})

    def test_encrypt_decrypt_message(self):
        # Test encryption and decryption functions
        plaintext = "Hello, world!"
        encrypted_text = encrypt_message(plaintext)
        decrypted_text = decrypt_message(encrypted_text)

        # Assertions
        self.assertNotEqual(plaintext, encrypted_text)  # Check that encryption changes the text
        self.assertEqual(decrypted_text, plaintext)   # Check that decryption retrieves the original text

if __name__ == '__main__':
    unittest.main()
