import unittest
from unittest.mock import patch, MagicMock
from src.runtime_checks import runtime_integrity_check
from src.utilities import secure_api_request, load_config

class TestRuntimeChecks(unittest.TestCase):

    def setUp(self):
        # Setup any necessary resources or initializations
        pass

    def tearDown(self):
        # Clean up after each test if necessary
        pass

    @patch('src.utilities.load_config')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('src.utilities.secure_api_request')
    def test_runtime_integrity_check_success(self, mock_secure_api_request, mock_open, mock_load_config):
        # Mocking configuration and file read
        mock_load_config.return_value = {'integrity_check_files': ['test_file.txt']}
        mock_open.return_value.__enter__.return_value.read.return_value = b'Test file content'
        mock_secure_api_request.return_value = {'status': 'ok'}

        # Call the function under test
        runtime_integrity_check()

        # Assertions
        mock_load_config.assert_called_once()
        mock_open.assert_called_once_with('test_file.txt', 'rb')
        mock_secure_api_request.assert_called_once_with('verify-file', {'file_path': 'test_file.txt', 'hash': '3a9b9e8ee262bcf2ff3a70cc5c4c9b276c18b4c64a5a9b70d7cf4e5f8a98ea71'})
    
    @patch('src.utilities.load_config')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('src.utilities.secure_api_request')
    def test_runtime_integrity_check_failure(self, mock_secure_api_request, mock_open, mock_load_config):
        # Mocking configuration and file read
        mock_load_config.return_value = {'integrity_check_files': ['test_file.txt']}
        mock_open.return_value.__enter__.return_value.read.return_value = b'Test file content'
        mock_secure_api_request.return_value = {'status': 'error'}

        # Call the function under test
        with self.assertRaises(Exception):
            runtime_integrity_check()

        # Assertions
        mock_load_config.assert_called_once()
        mock_open.assert_called_once_with('test_file.txt', 'rb')
        mock_secure_api_request.assert_called_once_with('verify-file', {'file_path': 'test_file.txt', 'hash': '3a9b9e8ee262bcf2ff3a70cc5c4c9b276c18b4c64a5a9b70d7cf4e5f8a98ea71'})

if __name__ == '__main__':
    unittest.main()
