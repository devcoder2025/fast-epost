
import pytest
import asyncio
from src.queue.task_queue import TaskQueue, Task
from src.queue.worker import Worker

@pytest.fixture
async def task_queue():
    queue = TaskQueue()
    yield queue
    await queue.stop()

@pytest.fixture
async def worker(task_queue):
    worker = Worker(task_queue)
    yield worker
    await worker.stop()

@pytest.mark.asyncio
async def test_task_enqueue(task_queue):
    async def handler(payload):
        return payload['value'] * 2

    task_queue.register_handler('multiply', handler)
    task_id = await task_queue.enqueue('multiply', {'value': 5})
    assert task_id is not None
    
    task = await task_queue.get_result(task_id)
    assert task.status == 'pending'
    assert task.payload == {'value': 5}

@pytest.mark.asyncio
async def test_task_processing(task_queue):
    async def handler(payload):
        await asyncio.sleep(0.1)
        return payload['value'] * 2

    task_queue.register_handler('multiply', handler)
    task_id = await task_queue.enqueue('multiply', {'value': 5})
    
    # Start processing
    process_task = asyncio.create_task(task_queue.start())
    await asyncio.sleep(0.2)
    
    task = await task_queue.get_result(task_id)
    assert task.status == 'completed'
    assert task.result == 10

    await task_queue.stop()
    await process_task

@pytest.mark.asyncio
async def test_task_priority(task_queue):
    results = []
    async def handler(payload):
        results.append(payload['value'])
        return payload['value']

    task_queue.register_handler('priority_test', handler)
    await task_queue.enqueue('priority_test', {'value': 'low'}, priority=1)
    await task_queue.enqueue('priority_test', {'value': 'high'}, priority=2)
    
    process_task = asyncio.create_task(task_queue.start())
    await asyncio.sleep(0.1)
    
    assert results[0] == 'high'
    await task_queue.stop()
    await process_task

@pytest.mark.asyncio
async def test_worker_stats(worker, task_queue):
    async def handler(payload):
        await asyncio.sleep(0.1)
        return payload['value']

    task_queue.register_handler('test', handler)
    await task_queue.enqueue('test', {'value': 1})
    await task_queue.enqueue('test', {'value': 2})
    
    worker_task = asyncio.create_task(worker.start())
    await asyncio.sleep(0.2)
    
    stats = await worker.get_stats()
    assert stats['total_tasks'] == 2
    assert stats['completed'] > 0
    
    await worker.stop()
    await worker_task
