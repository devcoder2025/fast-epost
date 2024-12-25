
from typing import Dict, Optional
import asyncio
import aiohttp
from abc import ABC, abstractmethod
from .registry import ServiceRegistry, ServiceInstance

class ServiceProvider(ABC):
    @abstractmethod
    async def register_service(
        self,
        name: str,
        host: str,
        port: int,
        metadata: Dict = None
    ):
        pass

    @abstractmethod
    async def deregister_service(self, name: str, instance_id: str):
        pass

    @abstractmethod
    async def start_heartbeat(self):
        pass

class ConsulServiceProvider(ServiceProvider):
    def __init__(
        self,
        consul_host: str = "localhost",
        consul_port: int = 8500,
        heartbeat_interval: int = 30
    ):
        self.consul_url = f"http://{consul_host}:{consul_port}"
        self.heartbeat_interval = heartbeat_interval
        self.registered_services: Dict[str, ServiceInstance] = {}
        self._running = False

    async def register_service(
        self,
        name: str,
        host: str,
        port: int,
        metadata: Dict = None
    ):
        service_id = f"{name}-{host}:{port}"
        check = {
            "Name": f"Service '{name}' check",
            "TTL": f"{self.heartbeat_interval}s",
            "Status": "passing"
        }

        payload = {
            "ID": service_id,
            "Name": name,
            "Address": host,
            "Port": port,
            "Meta": metadata or {},
            "Check": check
        }

        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{self.consul_url}/v1/agent/service/register",
                json=payload
            ) as response:
                if response.status != 200:
                    raise Exception("Failed to register service with Consul")

        instance = ServiceInstance(
            id=service_id,
            name=name,
            host=host,
            port=port,
            metadata=metadata
        )
        self.registered_services[service_id] = instance
        return instance

    async def deregister_service(self, name: str, instance_id: str):
        if instance_id in self.registered_services:
            async with aiohttp.ClientSession() as session:
                async with session.put(
                    f"{self.consul_url}/v1/agent/service/deregister/{instance_id}"
                ) as response:
                    if response.status != 200:
                        raise Exception("Failed to deregister service from Consul")
            del self.registered_services[instance_id]

    async def start_heartbeat(self):
        self._running = True
        while self._running:
            for service_id, instance in self.registered_services.items():
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.put(
                            f"{self.consul_url}/v1/agent/check/pass/service:{service_id}"
                        ) as response:
                            if response.status != 200:
                                print(f"Failed to send heartbeat for {service_id}")
                except Exception as e:
                    print(f"Error sending heartbeat: {e}")
            
            await asyncio.sleep(self.heartbeat_interval / 2)

    async def stop_heartbeat(self):
        self._running = False
