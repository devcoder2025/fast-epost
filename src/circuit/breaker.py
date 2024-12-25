
from typing import Callable, Any, Optional, Dict
import asyncio
from functools import wraps
from .state import CircuitStateManager, CircuitState

class CircuitBreakerError(Exception):
    pass

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        half_open_max_calls: int = 3,
        excluded_exceptions: tuple = ()
    ):
        self.state_manager = CircuitStateManager(
            failure_threshold,
            recovery_timeout,
            half_open_max_calls
        )
        self.excluded_exceptions = excluded_exceptions

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await self.call(func, *args, **kwargs)
        return wrapper

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state_manager.state == CircuitState.OPEN:
            if not self.state_manager.attempt_reset():
                raise CircuitBreakerError("Circuit breaker is OPEN")

        try:
            result = await func(*args, **kwargs)
            self.state_manager.record_success()
            return result
        except Exception as e:
            if not isinstance(e, self.excluded_exceptions):
                self.state_manager.record_failure()
            raise

    @property
    def state(self) -> CircuitState:
        return self.state_manager.state

    def get_stats(self) -> Dict:
        stats = self.state_manager.stats
        return {
            'state': self.state.value,
            'failure_count': stats.failure_count,
            'success_count': stats.success_count,
            'total_requests': stats.total_requests,
            'last_failure_time': stats.last_failure_time,
            'last_success_time': stats.last_success_time
        }

    def reset(self):
        self.state_manager.reset()
