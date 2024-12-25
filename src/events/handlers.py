
from typing import Any, Callable, Dict
import asyncio
from dataclasses import dataclass
from .bus import Event

@dataclass
class HandlerMetrics:
    total_processed: int = 0
    total_failed: int = 0
    average_processing_time: float = 0.0
    last_processing_time: float = 0.0

class EventHandler:
    def __init__(self, func: Callable):
        self.func = func
        self.metrics = HandlerMetrics()
        self._running = True

    async def __call__(self, event: Event) -> Any:
        start_time = asyncio.get_event_loop().time()
        
        try:
            result = await self.func(event)
            self.metrics.total_processed += 1
            return result
        except Exception as e:
            self.metrics.total_failed += 1
            raise
        finally:
            processing_time = asyncio.get_event_loop().time() - start_time
            self.metrics.last_processing_time = processing_time
            self._update_average_time(processing_time)

    def _update_average_time(self, new_time: float):
        total_events = self.metrics.total_processed + self.metrics.total_failed
        if total_events == 1:
            self.metrics.average_processing_time = new_time
        else:
            self.metrics.average_processing_time = (
                (self.metrics.average_processing_time * (total_events - 1) + new_time)
                / total_events
            )

class RetryHandler(EventHandler):
    def __init__(
        self,
        func: Callable,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        super().__init__(func)
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    async def __call__(self, event: Event) -> Any:
        retries = 0
        while retries <= self.max_retries:
            try:
                return await super().__call__(event)
            except Exception as e:
                retries += 1
                if retries > self.max_retries:
                    raise
                await asyncio.sleep(self.retry_delay * retries)
