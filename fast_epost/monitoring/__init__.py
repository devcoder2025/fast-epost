import time
from contextlib import contextmanager
import logging
from .tracing import TracingSystem
from .metrics import MetricsCollector
from .dashboard import DashboardManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonitoringSystem:
    def __init__(self):
        self.tracer = TracingSystem()
        self.metrics = MetricsCollector()
        self.dashboard = DashboardManager()
        
    def monitor(self, f):
        @self.tracer.trace_request
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapped
