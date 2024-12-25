from typing import Optional, Callable
import asyncio
from functools import wraps
from .strategies import (
    RateLimitStrategy,
    FixedWindowStrategy,
    RateLimitResult
)

class RateLimiter:
    def __init__(
        self,
        strategy: Optional[RateLimitStrategy] = None,
        limit: int = 100,
        window: int = 60,
        key_func: Optional[Callable] = None
    ):
        self.strategy = strategy or FixedWindowStrategy()
        self.limit = limit
        self.window = window
        self.key_func = key_func or (lambda *args, **kwargs: "default")

    async def check_rate_limit(
        self,
        key: str
    ) -> RateLimitResult:
        return await self.strategy.check_rate_limit(
            key,
            self.limit,
            self.window
        )

    def rate_limit(
        self,
        limit: Optional[int] = None,
        window: Optional[int] = None,
        key_func: Optional[Callable] = None
    ):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Use provided values or fall back to instance defaults
                current_limit = limit or self.limit
                current_window = window or self.window
                current_key_func = key_func or self.key_func

                # Generate rate limit key
                key = current_key_func(*args, **kwargs)

                # Check rate limit
                result = await self.strategy.check_rate_limit(
                    key,
                    current_limit,
                    current_window
                )

                if not result.allowed:
                    raise RateLimitExceeded(
                        f"Rate limit exceeded. Try again in {result.reset_after:.1f} seconds"
                    )

                return await func(*args, **kwargs)
            return wrapper
        return decorator

class RateLimitExceeded(Exception):
    pass

class RateLimitMiddleware:
    def __init__(
        self,
        rate_limiter: RateLimiter,
        key_func: Optional[Callable] = None
    ):
        self.rate_limiter = rate_limiter
        self.key_func = key_func or (
            lambda request: f"{request.remote_addr}:{request.path}"
        )

    async def __call__(self, request, call_next):
        key = self.key_func(request)
        result = await self.rate_limiter.check_rate_limit(key)

        if not result.allowed:
            headers = {
                'X-RateLimit-Limit': str(result.limit),
                'X-RateLimit-Remaining': str(result.remaining),
                'X-RateLimit-Reset': str(int(result.reset_after)),
            }
            raise RateLimitExceeded(
                f"Rate limit exceeded. Try again in {result.reset_after:.1f} seconds",
                headers=headers
            )

        response = await call_next(request)
        response.headers.update({
            'X-RateLimit-Limit': str(result.limit),
            'X-RateLimit-Remaining': str(result.remaining),
            'X-RateLimit-Reset': str(int(result.reset_after)),
        })
        return response
