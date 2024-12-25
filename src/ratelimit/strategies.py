
from typing import Dict, Optional
import time
from dataclasses import dataclass
from collections import deque
import asyncio

@dataclass
class RateLimitResult:
    allowed: bool
    remaining: int
    reset_after: float
    limit: int

class TokenBucket:
    def __init__(self, rate: int, capacity: int):
        self.rate = rate  # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()

    async def acquire(self) -> RateLimitResult:
        now = time.time()
        time_passed = now - self.last_update
        self.tokens = min(
            self.capacity,
            self.tokens + time_passed * self.rate
        )
        self.last_update = now

        if self.tokens >= 1:
            self.tokens -= 1
            return RateLimitResult(
                allowed=True,
                remaining=int(self.tokens),
                reset_after=1 / self.rate,
                limit=self.capacity
            )
        
        return RateLimitResult(
            allowed=False,
            remaining=0,
            reset_after=(1 - self.tokens) / self.rate,
            limit=self.capacity
        )

class SlidingWindow:
    def __init__(self, max_requests: int, window_size: int):
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests = deque()

    async def acquire(self) -> RateLimitResult:
        now = time.time()
        
        # Remove expired timestamps
        while self.requests and self.requests[0] <= now - self.window_size:
            self.requests.popleft()

        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return RateLimitResult(
                allowed=True,
                remaining=self.max_requests - len(self.requests),
                reset_after=self.window_size - (now - self.requests[0] if self.requests else 0),
                limit=self.max_requests
            )

        oldest = self.requests[0]
        reset_after = self.window_size - (now - oldest)
        
        return RateLimitResult(
            allowed=False,
            remaining=0,
            reset_after=reset_after,
            limit=self.max_requests
        )

class FixedWindow:
    def __init__(self, max_requests: int, window_size: int):
        self.max_requests = max_requests
        self.window_size = window_size
        self.current_window = 0
        self.request_count = 0

    async def acquire(self) -> RateLimitResult:
        now = time.time()
        current_window = int(now / self.window_size)

        if current_window != self.current_window:
            self.current_window = current_window
            self.request_count = 0

        if self.request_count < self.max_requests:
            self.request_count += 1
            return RateLimitResult(
                allowed=True,
                remaining=self.max_requests - self.request_count,
                reset_after=self.window_size - (now % self.window_size),
                limit=self.max_requests
            )

        return RateLimitResult(
            allowed=False,
            remaining=0,
            reset_after=self.window_size - (now % self.window_size),
            limit=self.max_requests
        )
