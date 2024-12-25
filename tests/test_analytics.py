
import pytest
import asyncio
from unittest.mock import Mock, patch
from src.analytics.metrics import MetricsCollector, SystemMetrics, PackageMetrics
from src.analytics.dashboard import AnalyticsDashboard

@pytest.fixture
def metrics_collector():
    return MetricsCollector(history_size=10)

@pytest.fixture
def dashboard():
    return AnalyticsDashboard()

def test_metrics_collection(metrics_collector):
    with patch('psutil.cpu_percent', return_value=50.0):
        with patch('psutil.virtual_memory') as mock_memory:
            mock_memory.return_value.percent = 60.0
            metrics = metrics_collector._collect_system_metrics()
            
            assert isinstance(metrics, SystemMetrics)
            assert metrics.cpu_usage == 50.0
            assert metrics.memory_usage == 60.0

@pytest.mark.asyncio
async def test_metrics_history(metrics_collector):
    with patch('psutil.cpu_percent', return_value=50.0):
        await metrics_collector.start_collection()
        await asyncio.sleep(2)
        metrics_collector.stop_collection()
        
        assert len(metrics_collector.history) > 0
        assert isinstance(metrics_collector.history[0], SystemMetrics)

def test_package_metrics(metrics_collector):
    package_metrics = PackageMetrics(
        name="test-package",
        version="1.0.0",
        download_count=100,
        build_time=2.5,
        dependencies=5
    )
    
    metrics_collector.update_package_metrics("test-package", package_metrics)
    snapshot = metrics_collector.get_metrics_snapshot()
    
    assert "test-package" in snapshot['packages']
    assert snapshot['packages']['test-package']['download_count'] == 100

@pytest.mark.asyncio
async def test_dashboard_websocket():
    dashboard = AnalyticsDashboard()
    mock_websocket = Mock()
    mock_websocket.accept = asyncio.coroutine(lambda: None)
    mock_websocket.receive_text = asyncio.coroutine(lambda: "ping")
    mock_websocket.send_json = asyncio.coroutine(lambda: None)
    
    await dashboard.app.websocket_endpoint(mock_websocket)
    assert mock_websocket.send_json.called
