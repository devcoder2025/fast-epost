from typing import Dict, List
import subprocess
import logging

class CIPipeline:  
    def __init__(self):  
        self.logger = logging.getLogger('ci')  
        self.logger.info("CIPipeline initialized")  # Log initialization

    def run_tests(self):
        return subprocess.run(['pytest'], capture_output=True)
        
    def build_docker(self, tag: str):
        return subprocess.run(['docker', 'build', '-t', f'fast-epost:{tag}', '.'])
        
    def run_linting(self):
        return subprocess.run(['flake8'])

    def deploy(self, tag: str):
        self.logger.info(f"Deploying Docker image with tag: {tag}")  # Log deployment
        return subprocess.run(['docker', 'run', f'fast-epost:{tag}'])
