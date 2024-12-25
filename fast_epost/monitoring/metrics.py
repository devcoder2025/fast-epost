from dataclasses import dataclass
from datetime import datetime
import psutil
import time

@dataclass
class SystemMetrics:
    cpu_usage: float
    memory_usage: float
    request_count: int
    response_time: float
    timestamp: datetime

class MetricsCollector:
    def __init__(self):
        self.metrics = []
        
    def collect_metrics(self):
        return SystemMetrics(
            cpu_usage=psutil.cpu_percent(),
            memory_usage=psutil.virtual_memory().percent,
            request_count=self.get_request_count(),
            response_time=self.get_response_time(),
            timestamp=datetime.now()
        )
