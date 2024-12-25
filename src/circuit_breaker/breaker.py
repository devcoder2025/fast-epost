from typing import Optional, Callable, Any, Type
from functools import wraps
import asyncio
import logging
from .states import CircuitStateHandler, CircuitState

class CircuitBreakerError(Exception):
    pass

class CircuitOpenError(CircuitBreakerError):
    pass

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: float = 0.5,
        recovery_timeout: float = 30.0,
        success_threshold: int = 2,
        excluded_exceptions: Optional[tuple] = None,
        on_state_change: Optional[Callable] = None
    ):
        self.state_handler = CircuitStateHandler(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
            success_threshold=success_threshold,
            on_state_change=on_state_change
        )
        self.excluded_exceptions = excluded_exceptions or ()
        self.logger = logging.getLogger(__name__)

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await self.call(func, *args, **kwargs)
        return wrapper

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if not self.state_handler.can_execute():
            raise CircuitOpenError(
                f"Circuit breaker is OPEN - {func.__name__} call rejected"
            )

        try:
            result = await func(*args, **kwargs)
            self.state_handler.record_success()
            return result

        except Exception as e:
            if not isinstance(e, self.excluded_exceptions):
                self.state_handler.record_failure()
                self.logger.error(
                    f"Circuit breaker recorded failure in {func.__name__}: {str(e)}"
                )
            raise

    @property
    def state(self) -> CircuitState:
        return self.state_handler.state

    @property
    def stats(self):
        return self.state_handler.stats

class CircuitBreakerRegistry:
    def __init__(self):
        self.breakers = {}

    def get_or_create(
        self,
        name: str,
        **kwargs
    ) -> CircuitBreaker:
        if name not in self.breakers:
            self.breakers[name] = CircuitBreaker(**kwargs)
        return self.breakers[name]

    def get(self, name: str) -> Optional[CircuitBreaker]:
        return self.breakers.get(name)

    def reset(self, name: str):
        if name in self.breakers:
            del self.breakers[name]
