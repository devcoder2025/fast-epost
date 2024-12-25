class ErrorMonitor:
    def __init__(self):
        self.error_counts = {}
        self.alerts = []
        
    def track_error(self, error: AppError):
        self.error_counts[error.code] = self.error_counts.get(error.code, 0) + 1
        self._check_thresholds(error.code)
