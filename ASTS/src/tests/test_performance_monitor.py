import unittest
from unittest.mock import patch, MagicMock
from src.performance_monitor import monitor_cpu_usage, monitor_memory_usage

class TestPerformanceMonitor(unittest.TestCase):

    def setUp(self):
        # Setup any necessary resources or initializations
        pass

    def tearDown(self):
        # Clean up after each test if necessary
        pass

    @patch('src.performance_monitor.psutil.cpu_percent')
    def test_monitor_cpu_usage(self, mock_cpu_percent):
        mock_cpu_percent.return_value = 30.0
        cpu_usage = monitor_cpu_usage()
        self.assertIsInstance(cpu_usage, float, "CPU usage should be a float")
        self.assertEqual(cpu_usage, 30.0, "CPU usage should match mocked value")

    @patch('src.performance_monitor.psutil.virtual_memory')
    def test_monitor_memory_usage(self, mock_virtual_memory):
        mock_virtual_memory.return_value.percent = 50.0
        memory_usage = monitor_memory_usage()
        self.assertIsInstance(memory_usage, float, "Memory usage should be a float")
        self.assertEqual(memory_usage, 50.0, "Memory usage should match mocked value")

if __name__ == '__main__':
    unittest.main()
