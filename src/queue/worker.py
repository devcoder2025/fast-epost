
from typing import Optional, List
import asyncio
from .task_queue import TaskQueue, Task

class Worker:
    def __init__(
        self,
        queue: TaskQueue,
        max_concurrent_tasks: int = 5
    ):
        self.queue = queue
        self.max_concurrent_tasks = max_concurrent_tasks
        self.active_tasks: List[asyncio.Task] = []
        self._running = False

    async def start(self):
        self._running = True
        while self._running:
            if len(self.active_tasks) < self.max_concurrent_tasks:
                task = asyncio.create_task(self.queue.start())
                self.active_tasks.append(task)
            
            # Clean up completed tasks
            self.active_tasks = [t for t in self.active_tasks if not t.done()]
            await asyncio.sleep(0.1)

    async def stop(self):
        self._running = False
        await self.queue.stop()
        
        if self.active_tasks:
            for task in self.active_tasks:
                task.cancel()
            await asyncio.gather(*self.active_tasks, return_exceptions=True)

    async def get_stats(self) -> dict:
        tasks = self.queue.results.values()
        return {
            'total_tasks': len(tasks),
            'pending': sum(1 for t in tasks if t.status == 'pending'),
            'processing': sum(1 for t in tasks if t.status == 'processing'),
            'completed': sum(1 for t in tasks if t.status == 'completed'),
            'failed': sum(1 for t in tasks if t.status == 'failed'),
            'active_workers': len(self.active_tasks)
        }
