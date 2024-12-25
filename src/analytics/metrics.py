
from dataclasses import dataclass
from typing import Dict, List, Optional
import time
import psutil
import asyncio
from collections import deque

@dataclass
class SystemMetrics:
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, int]
    timestamp: float

@dataclass
class PackageMetrics:
    name: str
    version: str
    download_count: int
    build_time: float
    dependencies: int

class MetricsCollector:
    def __init__(self, history_size: int = 1000):
        self.history: deque = deque(maxlen=history_size)
        self.package_stats: Dict[str, PackageMetrics] = {}
        self._running = False

    async def start_collection(self):
        self._running = True
        while self._running:
            metrics = self._collect_system_metrics()
            self.history.append(metrics)
            await asyncio.sleep(1)

    def stop_collection(self):
        self._running = False

    def _collect_system_metrics(self) -> SystemMetrics:
        return SystemMetrics(
            cpu_usage=psutil.cpu_percent(),
            memory_usage=psutil.virtual_memory().percent,
            disk_usage=psutil.disk_usage('/').percent,
            network_io={
                'bytes_sent': psutil.net_io_counters().bytes_sent,
                'bytes_recv': psutil.net_io_counters().bytes_recv
            },
            timestamp=time.time()
        )

    def update_package_metrics(self, package_name: str, metrics: PackageMetrics):
        self.package_stats[package_name] = metrics

    def get_metrics_snapshot(self) -> Dict:
        latest = self.history[-1] if self.history else None
        return {
            'system': latest.__dict__ if latest else None,
            'packages': {name: stats.__dict__ for name, stats in self.package_stats.items()}
        }
