from typing import Optional, Dict, Any
import time
import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
import aioredis

@dataclass
class RateLimitResult:
    allowed: bool
    remaining: int
    reset_after: float
    limit: int

class RateLimitStrategy(ABC):
    @abstractmethod
    async def check_rate_limit(
        self,
        key: str,
        limit: int,
        window: int
    ) -> RateLimitResult:
        pass

class FixedWindowStrategy(RateLimitStrategy):
    def __init__(self):
        self.windows: Dict[str, Dict[str, Any]] = {}

    async def check_rate_limit(
        self,
        key: str,
        limit: int,
        window: int
    ) -> RateLimitResult:
        current_time = time.time()
        window_start = int(current_time / window) * window
        window_key = f"{key}:{window_start}"

        if window_key not in self.windows:
            self.windows[window_key] = {
                "count": 0,
                "start_time": window_start
            }

        window_data = self.windows[window_key]
        
        # Clean up old windows
        for old_key in list(self.windows.keys()):
            if int(old_key.split(':')[1]) < window_start:
                del self.windows[old_key]

        allowed = window_data["count"] < limit
        if allowed:
            window_data["count"] += 1

        return RateLimitResult(
            allowed=allowed,
            remaining=max(0, limit - window_data["count"]),
            reset_after=window_start + window - current_time,
            limit=limit
        )

class SlidingWindowStrategy(RateLimitStrategy):
    def __init__(self):
        self.requests: Dict[str, list] = {}

    async def check_rate_limit(
        self,
        key: str,
        limit: int,
        window: int
    ) -> RateLimitResult:
        current_time = time.time()
        window_start = current_time - window

        if key not in self.requests:
            self.requests[key] = []

        # Remove old requests
        self.requests[key] = [
            ts for ts in self.requests[key]
            if ts > window_start
        ]

        allowed = len(self.requests[key]) < limit
        if allowed:
            self.requests[key].append(current_time)

        return RateLimitResult(
            allowed=allowed,
            remaining=max(0, limit - len(self.requests[key])),
            reset_after=min(self.requests[key][0] + window - current_time
                          if self.requests[key] else window,
                          window),
            limit=limit
        )

class RedisRateLimitStrategy(RateLimitStrategy):
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0"
    ):
        self.redis_url = redis_url
        self._redis: Optional[aioredis.Redis] = None

    async def connect(self):
        if not self._redis:
            self._redis = await aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )

    async def check_rate_limit(
        self,
        key: str,
        limit: int,
        window: int
    ) -> RateLimitResult:
        if not self._redis:
            await self.connect()

        current_time = time.time()
        window_start = int(current_time / window) * window
        window_key = f"ratelimit:{key}:{window_start}"

        async with self._redis.pipeline() as pipe:
            try:
                # Get current count and increment if within limit
                current = await self._redis.get(window_key)
                count = int(current) if current else 0
                allowed = count < limit

                if allowed:
                    await pipe.incr(window_key)
                    await pipe.expire(window_key, window)
                    await pipe.execute()
                    count += 1

                return RateLimitResult(
                    allowed=allowed,
                    remaining=max(0, limit - count),
                    reset_after=window_start + window - current_time,
                    limit=limit
                )
            except Exception as e:
                print(f"Redis error: {e}")
                return RateLimitResult(
                    allowed=True,
                    remaining=limit,
                    reset_after=window,
                    limit=limit
                )
