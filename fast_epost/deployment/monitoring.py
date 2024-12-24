class DeploymentMonitor:
    def __init__(self):
        self.metrics = {}
        
    def track_deployment(self, stage: str, duration: float):
        self.metrics[stage] = duration
        
    def get_deployment_stats(self) -> Dict:
        return {
            'total_time': sum(self.metrics.values()),
            'stages': self.metrics
        }
