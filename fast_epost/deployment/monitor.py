class DeploymentMonitor:
    def __init__(self):
        self.metrics = {}
        
    def track_deployment(self, stage: str, duration: float):
        self.metrics[stage] = duration
        
    def get_stats(self) -> Dict:
        return self.metrics
