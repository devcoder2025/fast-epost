import pytest
from unittest.mock import patch, mock_open
from src.platform.detector import EnhancedPlatformDetector

@pytest.fixture
def detector():
    return EnhancedPlatformDetector()

def test_platform_detection(detector):
    info = detector.platform_info
    assert 'system' in info
    assert 'python_version' in info
    assert 'architecture' in info

def test_container_detection():
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = True
        detector = EnhancedPlatformDetector()
        assert detector.container_info['is_container']

def test_resource_limits(detector):
    limits = detector.resource_limits
    assert limits.cpu_count > 0
    assert limits.memory_limit > 0

def test_network_detection(detector):
    network = detector.network_info
    assert isinstance(network.interfaces, dict)
    assert isinstance(network.open_ports, list)

@pytest.mark.parametrize("cgroup_data,expected", [
    ("100000 100000", 100000),
    ("max 100000", None),
])
def test_cpu_quota_detection(cgroup_data, expected):
    with patch('builtins.open', mock_open(read_data=cgroup_data)):
        with patch('os.path.exists', return_value=True):
            detector = EnhancedPlatformDetector()
            assert detector.resource_limits.cpu_quota == expected

def test_kubernetes_detection():
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = True
        with patch('builtins.open', mock_open(read_data="default")):
            detector = EnhancedPlatformDetector()
            assert detector.container_info['orchestrator'] == 'kubernetes'

def test_full_info(detector):
    info = detector.get_full_info()
    assert 'platform' in info
    assert 'container' in info
    assert 'resources' in info
    assert 'network' in info
