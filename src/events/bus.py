
from typing import Dict, List, Callable, Any, Optional
import asyncio
from dataclasses import dataclass
import logging
import time

@dataclass
class Event:
    name: str
    data: Any
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

class EventBus:
    def __init__(self):
        self.handlers: Dict[str, List[Callable]] = {}
        self.middleware: List[Callable] = []
        self._running = False
        self.event_queue = asyncio.Queue()
        self.logger = logging.getLogger(__name__)

    def subscribe(self, event_name: str, handler: Callable):
        if event_name not in self.handlers:
            self.handlers[event_name] = []
        self.handlers[event_name].append(handler)

    def unsubscribe(self, event_name: str, handler: Callable):
        if event_name in self.handlers:
            self.handlers[event_name].remove(handler)
            if not self.handlers[event_name]:
                del self.handlers[event_name]

    def add_middleware(self, middleware: Callable):
        self.middleware.append(middleware)

    async def publish(self, event: Event):
        await self.event_queue.put(event)

    async def start(self):
        self._running = True
        while self._running:
            try:
                event = await self.event_queue.get()
                await self._process_event(event)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error processing event: {e}")

    async def stop(self):
        self._running = False

    async def _process_event(self, event: Event):
        if not self.handlers.get(event.name):
            return

        # Apply middleware
        for middleware in self.middleware:
            event = await middleware(event)
            if event is None:
                return

        # Execute handlers
        tasks = []
        for handler in self.handlers[event.name]:
            tasks.append(asyncio.create_task(handler(event)))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
