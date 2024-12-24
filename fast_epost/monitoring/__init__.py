
import time
from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        
    @contextmanager
    def measure(self, operation_name: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            duration = time.perf_counter() - start
            self.metrics[operation_name] = duration
            logger.info(f"Operation {operation_name} took {duration:.4f} seconds")
            
    def get_metrics(self):
        return self.metrics
