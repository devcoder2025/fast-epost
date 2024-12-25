import psutil
import aiohttp
from typing import Dict

async def check_memory() -> Dict:
    memory = psutil.virtual_memory()
    return {
        "total": memory.total,
        "available": memory.available,
        "percent": memory.percent,
        "threshold": 90
    }

async def check_cpu() -> Dict:
    cpu_percent = psutil.cpu_percent(interval=1)
    return {
        "usage_percent": cpu_percent,
        "threshold": 80
    }

async def check_disk() -> Dict:
    disk = psutil.disk_usage('/')
    return {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent,
        "threshold": 90
    }

async def check_external_service(url: str) -> Dict:
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        async with session.get(url) as response:
            response_time = time.time() - start_time
            return {
                "status_code": response.status,
                "response_time": response_time,
                "threshold": 1.0
            }
