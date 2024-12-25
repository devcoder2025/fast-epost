
from typing import Dict, List, Optional
import asyncio
from dataclasses import dataclass
import time
import json
import aiohttp

@dataclass
class ServiceInstance:
    id: str
    name: str
    host: str
    port: int
    metadata: Dict
    health_check_url: str
    last_heartbeat: float
    status: str = 'UP'

class ServiceRegistry:
    def __init__(self, heartbeat_timeout: int = 30):
        self.services: Dict[str, Dict[str, ServiceInstance]] = {}
        self.heartbeat_timeout = heartbeat_timeout
        self._running = False

    async def register_service(
        self,
        name: str,
        host: str,
        port: int,
        metadata: Dict = None,
        health_check_url: Optional[str] = None
    ) -> str:
        instance_id = f"{name}-{host}:{port}"
        
        if name not in self.services:
            self.services[name] = {}
            
        self.services[name][instance_id] = ServiceInstance(
            id=instance_id,
            name=name,
            host=host,
            port=port,
            metadata=metadata or {},
            health_check_url=health_check_url or f"http://{host}:{port}/health",
            last_heartbeat=time.time()
        )
        
        return instance_id

    def deregister_service(self, name: str, instance_id: str):
        if name in self.services and instance_id in self.services[name]:
            del self.services[name][instance_id]
            if not self.services[name]:
                del self.services[name]

    def get_service(self, name: str) -> List[ServiceInstance]:
        return list(self.services.get(name, {}).values())

    async def start(self):
        self._running = True
        while self._running:
            await self._check_services_health()
            await asyncio.sleep(self.heartbeat_timeout / 2)

    def stop(self):
        self._running = False

    async def heartbeat(self, name: str, instance_id: str):
        if (name in self.services and 
            instance_id in self.services[name]):
            self.services[name][instance_id].last_heartbeat = time.time()
            return True
        return False

    async def _check_services_health(self):
        current_time = time.time()
        for service_name in list(self.services.keys()):
            for instance_id, instance in list(self.services[service_name].items()):
                if current_time - instance.last_heartbeat > self.heartbeat_timeout:
                    instance.status = 'DOWN'
                    await self._verify_health(instance)

    async def _verify_health(self, instance: ServiceInstance):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(instance.health_check_url) as response:
                    if response.status == 200:
                        instance.status = 'UP'
                        instance.last_heartbeat = time.time()
                    else:
                        self.deregister_service(instance.name, instance.id)
        except Exception:
            self.deregister_service(instance.name, instance.id)
