import unittest
from src.anti_debugging import anti_debugging

class TestAntiDebugging(unittest.TestCase):

    def test_anti_debugging(self):
        # Assuming the function should return True if anti-debugging measures are active
        self.assertTrue(anti_debugging())

if __name__ == '__main__':
    unittest.main()
