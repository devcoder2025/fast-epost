
from typing import List, Optional
import asyncio
import random
import aiohttp
from .registry import ServiceRegistry, ServiceInstance

class ServiceDiscoveryClient:
    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
        self.cache: Dict[str, List[ServiceInstance]] = {}
        self.cache_timeout = 60
        self.last_cache_update = 0

    async def get_service_instances(
        self,
        service_name: str,
        refresh: bool = False
    ) -> List[ServiceInstance]:
        if refresh or self._should_refresh_cache(service_name):
            self.cache[service_name] = self.registry.get_service(service_name)
            self.last_cache_update = time.time()
        return self.cache.get(service_name, [])

    async def get_service_instance(
        self,
        service_name: str,
        strategy: str = 'random'
    ) -> Optional[ServiceInstance]:
        instances = await self.get_service_instances(service_name)
        if not instances:
            return None

        active_instances = [i for i in instances if i.status == 'UP']
        if not active_instances:
            return None

        if strategy == 'random':
            return random.choice(active_instances)
        elif strategy == 'round_robin':
            return self._round_robin_select(active_instances)
        
        return active_instances[0]

    def _should_refresh_cache(self, service_name: str) -> bool:
        return (
            service_name not in self.cache or
            time.time() - self.last_cache_update > self.cache_timeout
        )

    def _round_robin_select(
        self,
        instances: List[ServiceInstance]
    ) -> ServiceInstance:
        if not hasattr(self, '_rr_counter'):
            self._rr_counter = 0
        self._rr_counter = (self._rr_counter + 1) % len(instances)
        return instances[self._rr_counter]

    async def call_service(
        self,
        service_name: str,
        path: str,
        method: str = 'GET',
        **kwargs
    ) -> Optional[Dict]:
        instance = await self.get_service_instance(service_name)
        if not instance:
            raise ServiceUnavailableError(f"No available instances for {service_name}")

        url = f"http://{instance.host}:{instance.port}{path}"
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                return await response.json()

class ServiceUnavailableError(Exception):
    pass
