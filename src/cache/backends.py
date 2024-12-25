from typing import Any, Optional, Dict
import time
import asyncio
import redis
from dataclasses import dataclass

@dataclass
class CacheEntry:
    value: Any
    expiry: Optional[float]

class MemoryCache:
    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
        self._running = False

    async def start(self):
        self._running = True
        asyncio.create_task(self._cleanup_loop())

    async def stop(self):
        self._running = False

    async def get(self, key: str) -> Any:
        entry = self._cache.get(key)
        if entry and (entry.expiry is None or entry.expiry > time.time()):
            return entry.value
        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        expiry = time.time() + ttl if ttl else None
        self._cache[key] = CacheEntry(value, expiry)

    async def delete(self, key: str):
        self._cache.pop(key, None)

    async def clear(self):
        self._cache.clear()

    async def _cleanup_loop(self):
        while self._running:
            current_time = time.time()
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry.expiry and entry.expiry <= current_time
            ]
            for key in expired_keys:
                del self._cache[key]
            await asyncio.sleep(1)

class RedisCache:
    def __init__(self, host: str = 'localhost', port: int = 6379):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)

    async def get(self, key: str) -> Any:
        return self.redis.get(key)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        self.redis.set(key, value, ex=ttl)

    async def delete(self, key: str):
        self.redis.delete(key)

    async def clear(self):
        self.redis.flushdb()
