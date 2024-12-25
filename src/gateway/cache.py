from typing import Dict, Optional
import time
import asyncio

class CacheManager:
    def __init__(self, ttl: int = 300):  # 5 minutes default TTL
        self.cache: Dict[str, Dict] = {}
        self.ttl = ttl

    async def get(self, key: str) -> Optional[Dict]:
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.ttl:
                return entry['data']
            del self.cache[key]
        return None

    async def set(self, key: str, value: Dict):
        self.cache[key] = {
            'data': value,
            'timestamp': time.time()
        }
