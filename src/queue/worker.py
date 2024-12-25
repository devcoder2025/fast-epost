from typing import Callable, Dict
import asyncio
from .core import MessageQueue, QueuePriority

class Worker:
    def __init__(self, queue: MessageQueue, max_retries: int = 3):
        self.queue = queue
        self.max_retries = max_retries
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

    async def process_message(self, queue_name: str, message: aio_pika.IncomingMessage):
        async with message.process():
            retry_count = message.headers.get('x-retry-count', 0)
            try:
                body = json.loads(message.body.decode())
                await self.handlers[queue_name](body['data'])
                self.queue.metrics.increment_processed()
            except Exception as e:
                if retry_count < self.max_retries:
                    await self._retry_message(message, retry_count + 1)
                else:
                    await self._move_to_dlq(message)
                self.queue.metrics.increment_failed()

    async def _retry_message(self, message: aio_pika.IncomingMessage, retry_count: int):
        await asyncio.sleep(self.queue.dlq.retry_intervals[retry_count - 1])
        await self.queue.channel.default_exchange.publish(
            aio_pika.Message(
                body=message.body,
                headers={'x-retry-count': retry_count}
            ),
            routing_key=message.routing_key
        )