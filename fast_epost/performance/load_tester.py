import asyncio
import aiohttp
from dataclasses import dataclass
from typing import List, Dict
import time

@dataclass
class LoadTestResult:
    requests_per_second: float
    average_response_time: float
    error_rate: float
    status_codes: Dict[int, int]

class LoadTester:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.results: List[LoadTestResult] = []
        
    async def run_test(self, concurrent_users: int, duration: int):
        start_time = time.time()
        tasks = []
        async with aiohttp.ClientSession() as session:
            for _ in range(concurrent_users):
                task = asyncio.create_task(self._user_session(session))
                tasks.append(task)
            await asyncio.gather(*tasks)
