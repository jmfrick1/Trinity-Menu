import unittest
from src.authentication import authenticate, generate_2fa_code, verify_2fa_code

class TestAuthentication(unittest.TestCase):
    def test_authenticate_success(self):
        self.assertTrue(authenticate("test_user", "test_password"))

    def test_authenticate_failure(self):
        self.assertFalse(authenticate("wrong_user", "wrong_password"))

    def test_2fa_code(self):
        secret = "JBSWY3DPEHPK3PXP"
        code = generate_2fa_code(secret)
        self.assertTrue(verify_2fa_code(secret, code))

if __name__ == '__main__':
    unittest.main()
