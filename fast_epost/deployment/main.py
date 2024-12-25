from .ci import CIPipeline
from .cd import CDPipeline
from .docker import DockerManager
from .monitor import DeploymentMonitor

class DeploymentOrchestrator:
    def __init__(self):
        self.ci = CIPipeline()
        self.cd = CDPipeline()
        self.docker = DockerManager()
        self.monitor = DeploymentMonitor()
        
    def run_deployment(self, environment: str, version: str):
        # Run CI Pipeline
        self.ci.run_tests()
        self.ci.run_linting()
        
        # Build and Push Docker Image
        self.docker.build_image(version)
        self.docker.push_image(version)
        
        # Deploy to Environment
        self.cd.deploy(environment)
        
        # Track Metrics
        self.monitor.track_deployment('complete', time.time())
