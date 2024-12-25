from typing import Dict, List
import asyncio
import logging

class CDPipeline:
    def __init__(self, config: Dict):
        self.config = config
        self.environments = ['staging', 'production']
        self.logger = logging.getLogger('cd_pipeline')
        
    async def deploy(self, environment: str, version: str):
        if environment not in self.environments:
            raise ValueError(f"Invalid environment: {environment}")
            
        steps = [
            self._prepare_deployment(environment, version),
            self._update_services(environment),
            self._run_migrations(environment),
            self._health_check(environment)
        ]
        
        for step in steps:
            success = await step
            if not success:
                self.logger.error(f"Deployment to {environment} failed")
                return False
        
        self.logger.info(f"Deployment to {environment} successful")
        return True
        
    async def _prepare_deployment(self, environment: str, version: str) -> bool:
        try:
            subprocess.run(['docker', 'tag', f'fast-epost:{version}', 
                          f'fast-epost:{environment}'], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
            
    async def _update_services(self, environment: str) -> bool:
        try:
            subprocess.run(['kubectl', 'apply', '-f', 
                          f'deployment/{environment}.yaml'], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
            
    async def _run_migrations(self, environment: str) -> bool:
        try:
            subprocess.run(['python', 'manage.py', 'migrate', 
                          '--database', environment], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
            
    async def _health_check(self, environment: str) -> bool:
        try:
            url = self.config[environment]['health_check_url']
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return response.status == 200
        except Exception:
            return False
