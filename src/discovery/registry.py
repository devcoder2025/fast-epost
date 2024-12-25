from typing import Dict, List, Optional, Set
import asyncio
import time
from dataclasses import dataclass
import json
import aiohttp

@dataclass
class ServiceInstance:
    id: str
    name: str
    host: str
    port: int
    metadata: Dict = None
    last_heartbeat: float = None
    status: str = "up"

class ServiceRegistry:
    def __init__(self, heartbeat_interval: int = 30, cleanup_interval: int = 60):
        self.services: Dict[str, Dict[str, ServiceInstance]] = {}
        self.heartbeat_interval = heartbeat_interval
        self.cleanup_interval = cleanup_interval
        self.watchers: Dict[str, Set[callable]] = {}
        self._running = False

    async def register(
        self,
        name: str,
        host: str,
        port: int,
        metadata: Dict = None
    ) -> ServiceInstance:
        instance_id = f"{name}-{host}:{port}"
        instance = ServiceInstance(
            id=instance_id,
            name=name,
            host=host,
            port=port,
            metadata=metadata or {},
            last_heartbeat=time.time()
        )

        if name not in self.services:
            self.services[name] = {}
        self.services[name][instance_id] = instance

        await self._notify_watchers(name, "register", instance)
        return instance

    async def deregister(self, name: str, instance_id: str):
        if name in self.services and instance_id in self.services[name]:
            instance = self.services[name].pop(instance_id)
            if not self.services[name]:
                del self.services[name]
            await self._notify_watchers(name, "deregister", instance)

    async def heartbeat(self, name: str, instance_id: str):
        if name in self.services and instance_id in self.services[name]:
            self.services[name][instance_id].last_heartbeat = time.time()
            self.services[name][instance_id].status = "up"
            return True
        return False

    def get_instances(self, name: str) -> List[ServiceInstance]:
        return list(self.services.get(name, {}).values())

    def watch(self, name: str, callback: callable):
        if name not in self.watchers:
            self.watchers[name] = set()
        self.watchers[name].add(callback)

    def unwatch(self, name: str, callback: callable):
        if name in self.watchers:
            self.watchers[name].discard(callback)
            if not self.watchers[name]:
                del self.watchers[name]

    async def _notify_watchers(
        self,
        name: str,
        event: str,
        instance: ServiceInstance
    ):
        if name in self.watchers:
            for callback in self.watchers[name]:
                try:
                    await callback(event, instance)
                except Exception as e:
                    print(f"Error notifying watcher: {e}")

    async def start(self):
        self._running = True
        asyncio.create_task(self._cleanup_loop())

    async def stop(self):
        self._running = False

    async def _cleanup_loop(self):
        while self._running:
            await self._cleanup_expired_services()
            await asyncio.sleep(self.cleanup_interval)

    async def _cleanup_expired_services(self):
        now = time.time()
        expired_timeout = now - (self.heartbeat_interval * 2)

        for service_name in list(self.services.keys()):
            for instance_id, instance in list(self.services[service_name].items()):
                if instance.last_heartbeat < expired_timeout:
                    instance.status = "down"
                    await self._notify_watchers(
                        service_name,
                        "expired",
                        instance
                    )
