from typing import Any, Optional, List
import asyncio
from functools import wraps
from .backends import CacheBackend, MemoryCache

class CacheManager:
    def __init__(self, backend: CacheBackend = None):
        self.backend = backend or MemoryCache()
        self.key_prefix = "cache:"

    def _build_key(self, key: str) -> str:
        return f"{self.key_prefix}{key}"

    async def get(self, key: str, default: Any = None) -> Any:
        value = await self.backend.get(self._build_key(key))
        return value if value is not None else default

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        await self.backend.set(self._build_key(key), value, ttl)

    async def delete(self, key: str):
        await self.backend.delete(self._build_key(key))

    async def clear(self):
        await self.backend.clear()

    def cached(self, ttl: Optional[int] = None, key_prefix: Optional[str] = None):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key
                if key_prefix:
                    cache_key = f"{key_prefix}:"
                else:
                    cache_key = f"{func.__module__}:{func.__name__}:"
                
                # Add args and kwargs to cache key
                cache_key += ":".join(str(arg) for arg in args)
                if kwargs:
                    cache_key += ":" + ":".join(
                        f"{k}={v}" for k, v in sorted(kwargs.items())
                    )

                # Try to get from cache
                cached_value = await self.get(cache_key)
                if cached_value is not None:
                    return cached_value

                # Execute function and cache result
                result = await func(*args, **kwargs)
                await self.set(cache_key, result, ttl)
                return result

            return wrapper
        return decorator

class CachePattern:
    @staticmethod
    def cache_aside(cache_manager: CacheManager, ttl: Optional[int] = None):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                cache_key = f"{func.__name__}:{args}:{kwargs}"
                result = await cache_manager.get(cache_key)
                
                if result is None:
                    result = await func(*args, **kwargs)
                    await cache_manager.set(cache_key, result, ttl)
                
                return result
            return wrapper
        return decorator

    @staticmethod
    def write_through(cache_manager: CacheManager, ttl: Optional[int] = None):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                result = await func(*args, **kwargs)
                cache_key = f"{func.__name__}:{args}:{kwargs}"
                await cache_manager.set(cache_key, result, ttl)
                return result
            return wrapper
        return decorator