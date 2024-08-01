import unittest
from unittest.mock import patch, MagicMock
from src.obfuscation import obfuscate_code, deobfuscate_code

class TestObfuscation(unittest.TestCase):

    def setUp(self):
        # Setup any necessary resources or initializations
        pass

    def tearDown(self):
        # Clean up after each test if necessary
        pass

    def test_obfuscate_code(self):
        # Test case for obfuscating code
        original_code = "print('Hello, World!')"
        obfuscated_code = obfuscate_code(original_code)
        self.assertNotEqual(original_code, obfuscated_code, "Obfuscated code should not be the same as original")
        self.assertIsInstance(obfuscated_code, str, "Obfuscated code should be a string")

    def test_deobfuscate_code(self):
        # Test case for deobfuscating code
        original_code = "print('Hello, World!')"
        obfuscated_code = obfuscate_code(original_code)
        deobfuscated_code = deobfuscate_code(obfuscated_code)
        self.assertEqual(original_code, deobfuscated_code, "Deobfuscated code should match original")
        self.assertIsInstance(deobfuscated_code, str, "Deobfuscated code should be a string")

if __name__ == '__main__':
    unittest.main()
