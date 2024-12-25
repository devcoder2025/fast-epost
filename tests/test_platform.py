import unittest
from unittest.mock import patch, mock_open
from src.platform.detector import PlatformDetector, PlatformInfo

class TestPlatformDetector(unittest.TestCase):
    def setUp(self):
        self.detector = PlatformDetector()

    @patch('platform.system')
    def test_system_detection(self, mock_system):
        mock_system.return_value = 'Linux'
        with patch('builtins.open', mock_open(read_data='ID="ubuntu"')):
            info = self.detector.detect()
            self.assertEqual(info.system, 'ubuntu')

    @patch('platform.machine')
    def test_architecture_detection(self, mock_machine):
        mock_machine.return_value = 'x86_64'
        info = self.detector.detect()
        self.assertEqual(info.architecture, 'amd64')

    @patch('os.cpu_count')
    def test_cpu_detection(self, mock_cpu_count):
        mock_cpu_count.return_value = 4
        info = self.detector.detect()
        self.assertEqual(info.cpu_count, 4)

    @patch('os.path.exists')
    def test_container_detection(self, mock_exists):
        mock_exists.return_value = True
        info = self.detector.detect()
        self.assertIsNotNone(info.container_info)

    def test_memory_detection(self):
        info = self.detector.detect()
        self.assertIsInstance(info.memory_gb, float)

    @patch('platform.system')
    @patch('platform.machine')
    def test_macos_detection(self, mock_machine, mock_system):
        mock_system.return_value = 'Darwin'
        mock_machine.return_value = 'arm64'
        info = self.detector.detect()
        self.assertEqual(info.system, 'macos')
        self.assertEqual(info.architecture, 'arm64')

    def test_platform_info_immutability(self):
        info1 = self.detector.detect()
        info2 = self.detector.detect()
        self.assertEqual(info1, info2)
