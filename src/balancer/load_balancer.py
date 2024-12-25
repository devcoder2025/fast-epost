
from typing import List, Dict, Optional
import asyncio
import random
from .health_check import HealthChecker
import aiohttp
from dataclasses import dataclass

@dataclass
class ServerStats:
    requests: int = 0
    errors: int = 0
    total_response_time: float = 0.0

class LoadBalancer:
    def __init__(self, servers: List[str]):
        self.health_checker = HealthChecker()
        self.stats: Dict[str, ServerStats] = {}
        self._initialize_servers(servers)

    def _initialize_servers(self, servers: List[str]):
        for server in servers:
            self.stats[server] = ServerStats()
            asyncio.create_task(self.health_checker.add_server(server))

    async def start(self):
        await asyncio.create_task(self.health_checker.start_monitoring())

    async def stop(self):
        await self.health_checker.stop_monitoring()

    async def handle_request(self, path: str, method: str = 'GET', data: Dict = None) -> Optional[Dict]:
        server = self._select_server()
        if not server:
            raise NoHealthyServersError("No healthy servers available")

        try:
            response = await self._forward_request(server, path, method, data)
            self._update_stats(server, True, response.get('response_time', 0))
            return response
        except Exception as e:
            self._update_stats(server, False, 0)
            raise

    def _select_server(self) -> Optional[str]:
        healthy_servers = self.health_checker.get_healthy_servers()
        if not healthy_servers:
            return None

        # Weighted random selection based on performance
        weights = []
        for server in healthy_servers:
            stats = self.stats[server]
            if stats.requests == 0:
                weights.append(1.0)
            else:
                avg_response_time = stats.total_response_time / stats.requests
                error_rate = stats.errors / stats.requests
                weight = 1.0 / (avg_response_time * (1 + error_rate))
                weights.append(weight)

        return random.choices(healthy_servers, weights=weights)[0]

    async def _forward_request(
        self,
        server: str,
        path: str,
        method: str,
        data: Optional[Dict]
    ) -> Dict:
        start_time = asyncio.get_event_loop().time()
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                f"{server}{path}",
                json=data
            ) as response:
                result = await response.json()
                result['response_time'] = asyncio.get_event_loop().time() - start_time
                return result

    def _update_stats(self, server: str, success: bool, response_time: float):
        stats = self.stats[server]
        stats.requests += 1
        if not success:
            stats.errors += 1
        stats.total_response_time += response_time

    def get_stats(self) -> Dict[str, Dict]:
        return {
            server: {
                'requests': stats.requests,
                'errors': stats.errors,
                'avg_response_time': (
                    stats.total_response_time / stats.requests
                    if stats.requests > 0 else 0
                )
            }
            for server, stats in self.stats.items()
        }

class NoHealthyServersError(Exception):
    pass
