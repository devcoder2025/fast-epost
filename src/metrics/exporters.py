
from typing import Dict, Any
import json
import aiohttp
import prometheus_client as prom
from abc import ABC, abstractmethod

class MetricsExporter(ABC):
    @abstractmethod
    async def export(self, metrics: Dict[str, Any]):
        pass

class PrometheusExporter(MetricsExporter):
    def __init__(self):
        self.gauges = {}
        self.counters = {}
        self.histograms = {}

    async def export(self, metrics: Dict[str, Any]):
        for name, data in metrics.items():
            metric_type = data['type']
            
            for labels_key, metric_data in data['values'].items():
                labels = metric_data['labels']
                
                if metric_type == 'gauge':
                    if name not in self.gauges:
                        self.gauges[name] = prom.Gauge(name, '', labels.keys())
                    self.gauges[name].labels(**labels).set(metric_data['value'])
                
                elif metric_type == 'counter':
                    if name not in self.counters:
                        self.counters[name] = prom.Counter(name, '', labels.keys())
                    self.counters[name].labels(**labels).inc(metric_data['value'])
                
                elif metric_type == 'histogram':
                    if name not in self.histograms:
                        self.histograms[name] = prom.Histogram(name, '', labels.keys())
                    self.histograms[name].labels(**labels).observe(metric_data['value'])

class JSONExporter(MetricsExporter):
    def __init__(self, filepath: str):
        self.filepath = filepath

    async def export(self, metrics: Dict[str, Any]):
        with open(self.filepath, 'w') as f:
            json.dump(metrics, f, indent=2)

class HTTPExporter(MetricsExporter):
    def __init__(self, url: str, headers: Dict[str, str] = None):
        self.url = url
        self.headers = headers or {}

    async def export(self, metrics: Dict[str, Any]):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url,
                json=metrics,
                headers=self.headers
            ) as response:
                if response.status not in (200, 201):
                    raise Exception(
                        f"Failed to export metrics: {response.status}"
                    )
