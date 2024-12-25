
from dataclasses import dataclass
from typing import Dict, List, Optional
import aiohttp
import asyncio
import time

@dataclass
class ServerHealth:
    url: str
    healthy: bool
    response_time: float
    last_check: float
    error_count: int = 0

class HealthChecker:
    def __init__(self, check_interval: int = 30):
        self.servers: Dict[str, ServerHealth] = {}
        self.check_interval = check_interval
        self._running = False

    async def add_server(self, url: str):
        self.servers[url] = ServerHealth(
            url=url,
            healthy=True,
            response_time=0,
            last_check=time.time()
        )

    async def start_monitoring(self):
        self._running = True
        while self._running:
            await self._check_all_servers()
            await asyncio.sleep(self.check_interval)

    async def stop_monitoring(self):
        self._running = False

    async def _check_all_servers(self):
        tasks = [
            self._check_server(url)
            for url in self.servers.keys()
        ]
        await asyncio.gather(*tasks)

    async def _check_server(self, url: str):
        start_time = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}/health") as response:
                    if response.status == 200:
                        self._update_server_status(
                            url,
                            healthy=True,
                            response_time=time.time() - start_time
                        )
                    else:
                        self._mark_server_unhealthy(url)
        except Exception:
            self._mark_server_unhealthy(url)

    def _update_server_status(
        self,
        url: str,
        healthy: bool,
        response_time: float
    ):
        server = self.servers[url]
        server.healthy = healthy
        server.response_time = response_time
        server.last_check = time.time()
        if healthy:
            server.error_count = 0

    def _mark_server_unhealthy(self, url: str):
        server = self.servers[url]
        server.healthy = False
        server.error_count += 1
        server.last_check = time.time()

    def get_healthy_servers(self) -> List[str]:
        return [
            url for url, health in self.servers.items()
            if health.healthy
        ]
