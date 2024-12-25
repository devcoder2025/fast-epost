from typing import Dict, List, Optional, Callable
import asyncio
import psutil
import time
from enum import Enum
from dataclasses import dataclass
import aiohttp
from datetime import datetime

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

@dataclass
class HealthCheck:
    name: str
    status: HealthStatus
    last_check: datetime
    details: Dict
    latency: float

class HealthMonitor:
    def __init__(self):
        self.checks: Dict[str, Callable] = {}
        self.results: Dict[str, HealthCheck] = {}
        self.check_interval: int = 30
        self._running = False

    async def add_check(self, name: str, check_func: Callable):
        self.checks[name] = check_func

    async def start(self):
        self._running = True
        while self._running:
            await self.run_checks()
            await asyncio.sleep(self.check_interval)

    async def stop(self):
        self._running = False

    async def run_checks(self):
        for name, check_func in self.checks.items():
            start_time = time.time()
            try:
                details = await check_func()
                status = HealthStatus.HEALTHY
            except Exception as e:
                details = {"error": str(e)}
                status = HealthStatus.UNHEALTHY

            self.results[name] = HealthCheck(
                name=name,
                status=status,
                last_check=datetime.utcnow(),
                details=details,
                latency=time.time() - start_time
            )

    def get_status(self) -> Dict:
        overall_status = HealthStatus.HEALTHY
        for result in self.results.values():
            if result.status == HealthStatus.UNHEALTHY:
                overall_status = HealthStatus.UNHEALTHY
                break
            elif result.status == HealthStatus.DEGRADED:
                overall_status = HealthStatus.DEGRADED

        return {
            "status": overall_status.value,
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {
                name: {
                    "status": check.status.value,
                    "last_check": check.last_check.isoformat(),
                    "latency": check.latency,
                    "details": check.details
                }
                for name, check in self.results.items()
            }
        }
