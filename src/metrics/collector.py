
from typing import Dict, List, Optional
import time
from dataclasses import dataclass, field
import asyncio
import statistics

@dataclass
class Metric:
    name: str
    value: float
    timestamp: float = field(default_factory=time.time)
    labels: Dict[str, str] = field(default_factory=dict)
    type: str = "gauge"  # gauge, counter, histogram

class MetricsCollector:
    def __init__(self):
        self.metrics: Dict[str, List[Metric]] = {}
        self.exporters = []
        self._running = False
        self._flush_interval = 10  # seconds

    def add_exporter(self, exporter):
        self.exporters.append(exporter)

    def gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        self._record_metric(name, value, "gauge", labels)

    def counter(self, name: str, value: float = 1, labels: Dict[str, str] = None):
        self._record_metric(name, value, "counter", labels)

    def histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        self._record_metric(name, value, "histogram", labels)

    def _record_metric(
        self,
        name: str,
        value: float,
        type: str,
        labels: Optional[Dict[str, str]] = None
    ):
        metric = Metric(name, value, time.time(), labels or {}, type)
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(metric)

    async def start(self):
        self._running = True
        while self._running:
            await self._flush_metrics()
            await asyncio.sleep(self._flush_interval)

    async def stop(self):
        self._running = False
        await self._flush_metrics()

    async def _flush_metrics(self):
        aggregated_metrics = self._aggregate_metrics()
        for exporter in self.exporters:
            try:
                await exporter.export(aggregated_metrics)
            except Exception as e:
                print(f"Error exporting metrics: {e}")
        self.metrics.clear()

    def _aggregate_metrics(self) -> Dict[str, Dict]:
        result = {}
        for name, metrics in self.metrics.items():
            if not metrics:
                continue

            by_labels = {}
            for metric in metrics:
                labels_key = tuple(sorted(metric.labels.items()))
                if labels_key not in by_labels:
                    by_labels[labels_key] = []
                by_labels[labels_key].append(metric)

            result[name] = {
                'type': metrics[0].type,
                'values': {}
            }

            for labels, labeled_metrics in by_labels.items():
                values = [m.value for m in labeled_metrics]
                labels_dict = dict(labels)

                if metrics[0].type == "gauge":
                    result[name]['values'][labels_key] = {
                        'value': values[-1],
                        'labels': labels_dict
                    }
                elif metrics[0].type == "counter":
                    result[name]['values'][labels_key] = {
                        'value': sum(values),
                        'labels': labels_dict
                    }
                elif metrics[0].type == "histogram":
                    result[name]['values'][labels_key] = {
                        'count': len(values),
                        'sum': sum(values),
                        'min': min(values),
                        'max': max(values),
                        'avg': statistics.mean(values),
                        'labels': labels_dict
                    }

        return result
