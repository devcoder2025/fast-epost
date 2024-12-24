from typing import List, Dict
import subprocess
import yaml

class DeploymentPipeline:
    def __init__(self):
        self.stages: List[str] = ['test', 'build', 'deploy']
        self.tasks: Dict[str, List[callable]] = {}
        
    def add_task(self, stage: str, task: callable):
        if stage not in self.tasks:
            self.tasks[stage] = []
        self.tasks[stage].append(task)
        
    async def run_pipeline(self):
        for stage in self.stages:
            for task in self.tasks[stage]:
                await task()
