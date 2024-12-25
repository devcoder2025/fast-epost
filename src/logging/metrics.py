from dataclasses import dataclass
from typing import Dict
import time

@dataclass
class MetricsCollector:
    def __init__(self):
        self.metrics: Dict[str, float] = {}
        self.start_times: Dict[str, float] = {}

    def start_operation(self, operation_name: str):
        self.start_times[operation_name] = time.time()

    def end_operation(self, operation_name: str):
        if operation_name in self.start_times:
            duration = time.time() - self.start_times[operation_name]
            self.metrics[operation_name] = duration
            del self.start_times[operation_name]

    def get_metrics(self) -> Dict[str, float]:
        return self.metrics.copy()
