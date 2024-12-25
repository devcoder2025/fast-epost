from prometheus_client import Counter, Histogram
import time

class AIMonitor:
    def __init__(self):
        self.prediction_counter = Counter('ai_predictions_total', 'Total predictions made')
        self.prediction_latency = Histogram('ai_prediction_latency', 'Prediction latency')
        self.batch_size_histogram = Histogram('ai_batch_size', 'Batch sizes processed')

class ScalableAI:
    def __init__(self, num_workers: int = 4):
        self.monitor = AIMonitor()
        self.workers = num_workers
        self.queue = mp.Queue()
        self.results = mp.Queue()
        self._start_workers()
        
    def _start_workers(self):
        self.processes = []
        for _ in range(self.workers):
            p = mp.Process(target=self._worker_loop)
            p.start()
            self.processes.append(p)
