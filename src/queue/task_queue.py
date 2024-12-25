
from typing import Any, Callable, Dict, Optional, List
import asyncio
import json
import time
from dataclasses import dataclass
import uuid

@dataclass
class Task:
    id: str
    name: str
    payload: Dict
    status: str
    created_at: float
    priority: int = 0
    retries: int = 0
    max_retries: int = 3
    result: Any = None
    error: Optional[str] = None

class TaskQueue:
    def __init__(self):
        self.tasks: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self.results: Dict[str, Task] = {}
        self.handlers: Dict[str, Callable] = {}
        self._running = False

    def register_handler(self, task_name: str, handler: Callable):
        self.handlers[task_name] = handler

    async def enqueue(
        self,
        task_name: str,
        payload: Dict,
        priority: int = 0
    ) -> str:
        if task_name not in self.handlers:
            raise ValueError(f"No handler registered for task: {task_name}")

        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            name=task_name,
            payload=payload,
            status='pending',
            created_at=time.time(),
            priority=priority
        )
        
        await self.tasks.put((-priority, task))
        self.results[task_id] = task
        return task_id

    async def get_result(self, task_id: str) -> Optional[Task]:
        return self.results.get(task_id)

    async def start(self):
        self._running = True
        while self._running:
            try:
                _, task = await self.tasks.get()
                await self._process_task(task)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error processing task: {e}")

    async def stop(self):
        self._running = False

    async def _process_task(self, task: Task):
        handler = self.handlers[task.name]
        task.status = 'processing'
        
        try:
            task.result = await handler(task.payload)
            task.status = 'completed'
        except Exception as e:
            task.error = str(e)
            task.retries += 1
            
            if task.retries < task.max_retries:
                task.status = 'pending'
                await self.tasks.put((-task.priority, task))
            else:
                task.status = 'failed'

        self.results[task.id] = task
