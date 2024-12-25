from typing import Callable, Dict
import asyncio
from .core import MessageQueue, QueuePriority

class Worker:
    def __init__(self, queue: MessageQueue):
        self.queue = queue
        self.handlers: Dict[str, Callable] = {}
        self._running = False

    async def register_handler(self, queue_name: str, handler: Callable):
        self.handlers[queue_name] = handler
        await self.queue.subscribe(queue_name, handler)

    async def start(self):
        self._running = True
        await self.queue.connect()
        while self._running:
            await asyncio.sleep(0.1)

    async def stop(self):
        self._running = False
        await self.queue.close()

    async def get_stats(self) -> dict:
        tasks = self.queue.results.values()
        return {
            'total_tasks': len(tasks),
            'pending': sum(1 for t in tasks if t.status == 'pending'),
            'processing': sum(1 for t in tasks if t.status == 'processing'),
            'completed': sum(1 for t in tasks if t.status == 'completed'),
            'failed': sum(1 for t in tasks if t.status == 'failed'),
            'active_workers': len(self.handlers)
        }
