
import pytest
import asyncio
import json
import tempfile
from src.metrics.collector import MetricsCollector
from src.metrics.exporters import JSONExporter, PrometheusExporter

@pytest.fixture
def collector():
    return MetricsCollector()

@pytest.mark.asyncio
async def test_gauge_metrics(collector):
    collector.gauge("cpu_usage", 45.2, {"host": "server1"})
    collector.gauge("cpu_usage", 48.5, {"host": "server1"})
    
    metrics = collector._aggregate_metrics()
    assert metrics["cpu_usage"]["type"] == "gauge"
    assert metrics["cpu_usage"]["values"][tuple([("host", "server1")])]["value"] == 48.5

@pytest.mark.asyncio
async def test_counter_metrics(collector):
    collector.counter("requests_total", 1, {"endpoint": "/api"})
    collector.counter("requests_total", 1, {"endpoint": "/api"})
    
    metrics = collector._aggregate_metrics()
    assert metrics["requests_total"]["type"] == "counter"
    assert metrics["requests_total"]["values"][tuple([("endpoint", "/api")])]["value"] == 2

@pytest.mark.asyncio
async def test_histogram_metrics(collector):
    collector.histogram("response_time", 0.2, {"endpoint": "/api"})
    collector.histogram("response_time", 0.3, {"endpoint": "/api"})
    
    metrics = collector._aggregate_metrics()
    histogram_data = metrics["response_time"]["values"][tuple([("endpoint", "/api")])]
    assert metrics["response_time"]["type"] == "histogram"
    assert histogram_data["count"] == 2
    assert histogram_data["avg"] == 0.25

@pytest.mark.asyncio
async def test_json_exporter():
    with tempfile.NamedTemporaryFile() as tmp:
        collector = MetricsCollector()
        exporter = JSONExporter(tmp.name)
        collector.add_exporter(exporter)
        
        collector.gauge("test_metric", 123)
        await collector._flush_metrics()
        
        with open(tmp.name) as f:
            data = json.load(f)
            assert "test_metric" in data
            assert data["test_metric"]["type"] == "gauge"

@pytest.mark.asyncio
async def test_prometheus_exporter():
    collector = MetricsCollector()
    exporter = PrometheusExporter()
    collector.add_exporter(exporter)
    
    collector.gauge("test_gauge", 123, {"label": "value"})
    await collector._flush_metrics()
    
    assert "test_gauge" in exporter.gauges
    
@pytest.mark.asyncio
async def test_multiple_exporters(collector):
    with tempfile.NamedTemporaryFile() as tmp:
        json_exporter = JSONExporter(tmp.name)
        prom_exporter = PrometheusExporter()
        
        collector.add_exporter(json_exporter)
        collector.add_exporter(prom_exporter)
        
        collector.gauge("test_metric", 123)
        await collector._flush_metrics()
        
        # Verify JSON export
        with open(tmp.name) as f:
            data = json.load(f)
            assert "test_metric" in data
        
        # Verify Prometheus export
        assert "test_metric" in prom_exporter.gauges
