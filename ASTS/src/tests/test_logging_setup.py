import unittest
import logging
from src.utilities import get_logger

class TestLoggingSetup(unittest.TestCase):

    def setUp(self):
        # Setup any necessary resources or initializations
        pass

    def tearDown(self):
        # Clean up after each test if necessary
        pass

    def test_logger_creation(self):
        # Test if logger is created successfully
        logger = get_logger()
        self.assertIsInstance(logger, logging.Logger, "Logger should be an instance of logging.Logger")

    def test_logger_level(self):
        # Test if logger level is set to INFO
        logger = get_logger()
        self.assertEqual(logger.level, logging.INFO, "Logger level should be set to INFO")

    def test_logger_name(self):
        # Test if logger name is correctly set
        logger = get_logger()
        self.assertEqual(logger.name, "your_project_name", "Logger name should match your project's name")

if __name__ == '__main__':
    unittest.main()
