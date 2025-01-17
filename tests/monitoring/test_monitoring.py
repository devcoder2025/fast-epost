
import pytest
from unittest.mock import Mock, patch
from src.monitoring.metrics_collector import (
    SystemMetricsCollector,
    ApplicationMetricsCollector,
    BuildMetricsCollector
)
from src.monitoring.alerting import AlertManager, Alert

@pytest.fixture
def system_metrics():
    return SystemMetricsCollector()

@pytest.fixture
def app_metrics():
    return ApplicationMetricsCollector()

@pytest.fixture
def build_metrics():
    return BuildMetricsCollector()

@pytest.fixture
def alert_manager():
    return AlertManager()

def test_system_metrics_collection(system_metrics):
    with patch('psutil.cpu_percent', return_value=50.0):
        with patch('psutil.virtual_memory') as mock_memory:
            mock_memory.return_value.percent = 60.0
            system_metrics._collect_metrics()
            assert float(system_metrics.cpu_usage._value.get()) == 50.0
            assert float(system_metrics.memory_usage._value.get()) == 60.0

def test_application_metrics(app_metrics):
    app_metrics.track_request(0.5, 200)
    assert float(app_metrics.request_count._value.get()) == 1
    
    app_metrics.track_request(1.0, 500)
    assert float(app_metrics.error_count._value.get()) == 1

def test_build_metrics(build_metrics):
    build_metrics.record_build(30.0, True)
    assert float(build_metrics.build_success._value.get()) == 1
    
    build_metrics.record_build(45.0, False)
    assert float(build_metrics.build_failure._value.get()) == 1

@pytest.mark.asyncio
async def test_alert_manager(alert_manager):
    with patch.object(alert_manager, '_collect_current_metrics') as mock_metrics:
        mock_metrics.return_value = {'cpu_usage': 95.0}
        await alert_manager._check_thresholds()
        assert 'cpu_usage' in alert_manager.active_alerts
        assert alert_manager.active_alerts['cpu_usage'].severity == 'critical'

def test_alert_generation(alert_manager):
    alert = Alert(
        severity='critical',
        metric='cpu_usage',
        value=95.0,
        threshold=90.0,
        timestamp=datetime.now(),
        message='CPU usage critical'
    )
    assert 'CRITICAL' in alert_manager._generate_alert_message(
        alert.metric,
        alert.value,
        alert.threshold,
        alert.severity
    )
