import unittest
from unittest.mock import patch, MagicMock
from src.utilities import secure_api_request, load_config

class TestUtilities(unittest.TestCase):

    def setUp(self):
        # Setup any necessary resources or initializations
        pass

    def tearDown(self):
        # Clean up after each test if necessary
        pass

    @patch('src.utilities.requests.post')
    def test_secure_api_request_success(self, mock_post):
        # Mocking the requests.post method to simulate successful API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "ok"}

        # Call the function under test
        response = secure_api_request("test-endpoint", {"key": "value"})

        # Assertions
        mock_post.assert_called_once_with("https://api.example.com/test-endpoint", json={"key": "value"})
        self.assertEqual(response, {"status": "ok"})

    @patch('src.utilities.requests.post')
    def test_secure_api_request_failure(self, mock_post):
        # Mocking the requests.post method to simulate failed API response
        mock_post.return_value.status_code = 500

        # Call the function under test
        response = secure_api_request("test-endpoint", {"key": "value"})

        # Assertions
        mock_post.assert_called_once_with("https://api.example.com/test-endpoint", json={"key": "value"})
        self.assertIsNone(response)

    @patch('src.utilities.json.load')
    @patch('src.utilities.open')
    def test_load_config_success(self, mock_open, mock_json_load):
        # Mocking the open and json.load methods to simulate loading configuration
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_json_load.return_value = {"key": "value"}

        # Call the function under test
        config = load_config()

        # Assertions
        mock_open.assert_called_once_with('config.json', 'r')
        mock_json_load.assert_called_once_with(mock_file)
        self.assertEqual(config, {"key": "value"})

    @patch('src.utilities.json.load')
    @patch('src.utilities.open')
    def test_load_config_file_not_found(self, mock_open, mock_json_load):
        # Mocking the open and json.load methods to simulate file not found scenario
        mock_open.side_effect = FileNotFoundError

        # Call the function under test
        config = load_config()

        # Assertions
        mock_open.assert_called_once_with('config.json', 'r')
        mock_json_load.assert_not_called()
        self.assertEqual(config, {})  # Default empty config

if __name__ == '__main__':
    unittest.main()
