import time
from contextlib import contextmanager

class PerformanceMonitor:
    @contextmanager
    def measure(self, operation_name: str):
        start = time.perf_counter()
        yield
        duration = time.perf_counter() - start
        print(f"{operation_name}: {duration:.4f} seconds")
