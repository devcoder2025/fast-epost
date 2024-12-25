from typing import Any, Optional, Dict
from .backends import MemoryCache, RedisCache
import json

class CacheManager:
    def __init__(self, backend: str = 'memory', **kwargs):
        self.backend = self._create_backend(backend, **kwargs)
        self._key_prefix = 'cache:'

    def _create_backend(self, backend: str, **kwargs):
        if backend == 'memory':
            return MemoryCache()
        elif backend == 'redis':
            return RedisCache(**kwargs)
        else:
            raise ValueError(f"Unsupported cache backend: {backend}")

    async def start(self):
        if hasattr(self.backend, 'start'):
            await self.backend.start()

    async def stop(self):
        if hasattr(self.backend, 'stop'):
            await self.backend.stop()

    def _make_key(self, key: str) -> str:
        return f"{self._key_prefix}{key}"

    async def get(self, key: str, default: Any = None) -> Any:
        value = await self.backend.get(self._make_key(key))
        if value is None:
            return default
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ):
        try:
            serialized = json.dumps(value)
        except TypeError:
            serialized = str(value)
        await self.backend.set(self._make_key(key), serialized, ttl)

    async def delete(self, key: str):
        await self.backend.delete(self._make_key(key))

    async def clear(self):
        await self.backend.clear()

    async def get_or_set(
        self,
        key: str,
        default_func,
        ttl: Optional[int] = None
    ) -> Any:
        value = await self.get(key)
        if value is None:
            value = await default_func()
            await self.set(key, value, ttl)
        return value

    async def increment(self, key: str, amount: int = 1) -> int:
        value = await self.get(key, 0)
        new_value = value + amount
        await self.set(key, new_value)
        return new_value

    async def decrement(self, key: str, amount: int = 1) -> int:
        return await self.increment(key, -amount)
