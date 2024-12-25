
from typing import Dict, Optional
import asyncio
from .strategies import TokenBucket, SlidingWindow, FixedWindow, RateLimitResult

class RateLimiter:
    def __init__(self, strategy: str = 'token_bucket', **kwargs):
        self.limiters: Dict[str, Dict[str, object]] = {}
        self.strategy = strategy
        self.strategy_kwargs = kwargs

    def _create_limiter(self, strategy: str, **kwargs):
        if strategy == 'token_bucket':
            return TokenBucket(
                rate=kwargs.get('rate', 10),
                capacity=kwargs.get('capacity', 10)
            )
        elif strategy == 'sliding_window':
            return SlidingWindow(
                max_requests=kwargs.get('max_requests', 10),
                window_size=kwargs.get('window_size', 60)
            )
        elif strategy == 'fixed_window':
            return FixedWindow(
                max_requests=kwargs.get('max_requests', 10),
                window_size=kwargs.get('window_size', 60)
            )
        else:
            raise ValueError(f"Unknown rate limiting strategy: {strategy}")

    def get_limiter(self, key: str, namespace: str = 'default') -> object:
        if namespace not in self.limiters:
            self.limiters[namespace] = {}
        
        if key not in self.limiters[namespace]:
            self.limiters[namespace][key] = self._create_limiter(
                self.strategy,
                **self.strategy_kwargs
            )
            
        return self.limiters[namespace][key]

    async def acquire(
        self,
        key: str,
        namespace: str = 'default'
    ) -> RateLimitResult:
        limiter = self.get_limiter(key, namespace)
        return await limiter.acquire()

    async def is_allowed(
        self,
        key: str,
        namespace: str = 'default'
    ) -> bool:
        result = await self.acquire(key, namespace)
        return result.allowed

    def get_limit_headers(self, result: RateLimitResult) -> Dict[str, str]:
        return {
            'X-RateLimit-Limit': str(result.limit),
            'X-RateLimit-Remaining': str(result.remaining),
            'X-RateLimit-Reset': str(int(result.reset_after))
        }

    async def clear(self, namespace: str = 'default'):
        if namespace in self.limiters:
            del self.limiters[namespace]
