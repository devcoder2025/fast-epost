from dataclasses import dataclass
from typing import List, Dict
import docker
import subprocess
import logging

@dataclass
class CIStage:
    name: str
    commands: List[str]
    environment: Dict[str, str]
    timeout: int = 300

class CIRunner:
    def __init__(self):
        self.stages: List[CIStage] = []
        self.docker_client = docker.from_env()
        self.logger = logging.getLogger('ci_runner')
        
    def add_stage(self, stage: CIStage):
        self.stages.append(stage)
        
    async def run_pipeline(self):
        results = {}
        for stage in self.stages:
            self.logger.info(f"Running stage: {stage.name}")
            try:
                container = self.docker_client.containers.run(
                    'python:3.12',
                    command=stage.commands,
                    environment=stage.environment,
                    detach=True
                )
                result = container.wait(timeout=stage.timeout)
                results[stage.name] = result['StatusCode'] == 0
            except Exception as e:
                self.logger.error(f"Stage {stage.name} failed: {str(e)}")
                results[stage.name] = False
        return results
