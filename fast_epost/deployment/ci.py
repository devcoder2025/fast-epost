from typing import Dict, List
import subprocess
import logging

class CIPipeline:
    def __init__(self):
        self.logger = logging.getLogger('ci')
        
    def run_tests(self):
        return subprocess.run(['pytest'], capture_output=True)
        
    def build_docker(self, tag: str):
        return subprocess.run(['docker', 'build', '-t', f'fast-epost:{tag}', '.'])
        
    def run_linting(self):
        return subprocess.run(['flake8'])
