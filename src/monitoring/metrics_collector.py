
import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
import time
import psutil
import prometheus_client as prom

@dataclass
class MetricThreshold:
    warning: float
    critical: float

class SystemMetricsCollector:
    def __init__(self):
        self.cpu_usage = prom.Gauge('cpu_usage', 'CPU usage percentage')
        self.memory_usage = prom.Gauge('memory_usage', 'Memory usage percentage')
        self.disk_usage = prom.Gauge('disk_usage', 'Disk usage percentage')
        self.network_io = prom.Counter('network_io', 'Network IO bytes')
        
        self.thresholds = {
            'cpu': MetricThreshold(warning=70.0, critical=90.0),
            'memory': MetricThreshold(warning=80.0, critical=95.0),
            'disk': MetricThreshold(warning=85.0, critical=95.0)
        }
        
        self._running = False

    async def start_collection(self):
        self._running = True
        while self._running:
            self._collect_metrics()
            await asyncio.sleep(1)

    def stop_collection(self):
        self._running = False

    def _collect_metrics(self):
        # CPU metrics
        cpu_percent = psutil.cpu_percent()
        self.cpu_usage.set(cpu_percent)

        # Memory metrics
        memory = psutil.virtual_memory()
        self.memory_usage.set(memory.percent)

        # Disk metrics
        disk = psutil.disk_usage('/')
        self.disk_usage.set(disk.percent)

        # Network metrics
        network = psutil.net_io_counters()
        self.network_io.inc(network.bytes_sent + network.bytes_recv)

class ApplicationMetricsCollector:
    def __init__(self):
        self.request_count = prom.Counter(
            'app_request_total',
            'Total request count'
        )
        self.request_latency = prom.Histogram(
            'app_request_latency_seconds',
            'Request latency in seconds'
        )
        self.error_count = prom.Counter(
            'app_error_total',
            'Total error count'
        )
        self.active_users = prom.Gauge(
            'app_active_users',
            'Number of active users'
        )

    def track_request(self, duration: float, status_code: int):
        self.request_count.inc()
        self.request_latency.observe(duration)
        if status_code >= 400:
            self.error_count.inc()

    def update_active_users(self, count: int):
        self.active_users.set(count)

class BuildMetricsCollector:
    def __init__(self):
        self.build_duration = prom.Histogram(
            'build_duration_seconds',
            'Build duration in seconds'
        )
        self.build_success = prom.Counter(
            'build_success_total',
            'Total successful builds'
        )
        self.build_failure = prom.Counter(
            'build_failure_total',
            'Total failed builds'
        )
        self.build_queue_size = prom.Gauge(
            'build_queue_size',
            'Current build queue size'
        )

    def record_build(self, duration: float, success: bool):
        self.build_duration.observe(duration)
        if success:
            self.build_success.inc()
        else:
            self.build_failure.inc()

    def update_queue_size(self, size: int):
        self.build_queue_size.set(size)
