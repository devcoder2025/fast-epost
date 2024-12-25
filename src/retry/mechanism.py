from typing import TypeVar, Callable, Optional, Any
import asyncio
import logging
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta

T = TypeVar('T')

class RetryState(Enum):
    CLOSED = "closed"      # Circuit is closed, requests flow normally
    OPEN = "open"         # Circuit is open, requests fail fast
    HALF_OPEN = "half_open" # Testing if service is back to normal

@dataclass
class RetryPolicy:
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 30.0
    exponential_base: float = 2
    jitter: bool = True

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = RetryState.CLOSED
        
    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.failure_threshold:
            self.state = RetryState.OPEN

    def record_success(self):
        self.failure_count = 0
        self.state = RetryState.CLOSED

    def can_proceed(self) -> bool:
        if self.state == RetryState.CLOSED:
            return True
        
        if self.state == RetryState.OPEN:
            if self.last_failure_time and \
               (datetime.now() - self.last_failure_time) > timedelta(seconds=self.recovery_timeout):
                self.state = RetryState.HALF_OPEN
                return True
        
        return self.state == RetryState.HALF_OPEN

class RetryManager:
    def __init__(self, policy: RetryPolicy = RetryPolicy()):
        self.policy = policy
        self.circuit_breaker = CircuitBreaker()
        self.logger = logging.getLogger(__name__)

    async def execute(
        self,
        operation: Callable[..., T],
        *args,
        **kwargs
    ) -> T:
        if not self.circuit_breaker.can_proceed():
            raise Exception("Circuit breaker is open")

        attempt = 0
        last_exception = None
        
        while attempt < self.policy.max_attempts:
            try:
                result = await operation(*args, **kwargs)
                self.circuit_breaker.record_success()
                return result
                
            except Exception as e:
                attempt += 1
                last_exception = e
                self.circuit_breaker.record_failure()
                
                if attempt == self.policy.max_attempts:
                    self.logger.error(f"Operation failed after {attempt} attempts", exc_info=e)
                    raise

                delay = self._calculate_delay(attempt)
                self.logger.warning(
                    f"Attempt {attempt} failed, retrying in {delay:.2f} seconds",
                    exc_info=e
                )
                await asyncio.sleep(delay)
        
        raise last_exception if last_exception else Exception("Retry attempts exhausted")

    def _calculate_delay(self, attempt: int) -> float:
        delay = min(
            self.policy.initial_delay * (self.policy.exponential_base ** (attempt - 1)),
            self.policy.max_delay
        )
        
        if self.policy.jitter:
            delay *= (0.5 + asyncio.get_event_loop().time() % 1)
            
        return delay
