from typing import Any, Optional, Dict
import time
import asyncio
import aioredis
from abc import ABC, abstractmethod

class CacheBackend(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        pass

    @abstractmethod
    async def delete(self, key: str):
        pass

    @abstractmethod
    async def clear(self):
        pass

class MemoryCache(CacheBackend):
    def __init__(self):
        self.cache: Dict[str, tuple] = {}
        self._running = False

    async def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        
        value, expiry = self.cache[key]
        if expiry and time.time() > expiry:
            await self.delete(key)
            return None
            
        return value

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        expiry = time.time() + ttl if ttl else None
        self.cache[key] = (value, expiry)

    async def delete(self, key: str):
        self.cache.pop(key, None)

    async def clear(self):
        self.cache.clear()

    async def start_cleanup(self):
        self._running = True
        while self._running:
            current_time = time.time()
            expired_keys = [
                key for key, (_, expiry) in self.cache.items()
                if expiry and current_time > expiry
            ]
            for key in expired_keys:
                await self.delete(key)
            await asyncio.sleep(1)

    async def stop_cleanup(self):
        self._running = False

class RedisCache(CacheBackend):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        password: Optional[str] = None,
        db: int = 0
    ):
        self.redis_url = f"redis://{host}:{port}/{db}"
        self.password = password
        self._redis: Optional[aioredis.Redis] = None

    async def connect(self):
        self._redis = await aioredis.from_url(
            self.redis_url,
            password=self.password,
            encoding="utf-8",
            decode_responses=True
        )

    async def disconnect(self):
        if self._redis:
            await self._redis.close()

    async def get(self, key: str) -> Optional[Any]:
        if not self._redis:
            await self.connect()
        return await self._redis.get(key)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        if not self._redis:
            await self.connect()
        await self._redis.set(key, value, ex=ttl)

    async def delete(self, key: str):
        if not self._redis:
            await self.connect()
        await self._redis.delete(key)

    async def clear(self):
        if not self._redis:
            await self.connect()
        await self._redis.flushdb()