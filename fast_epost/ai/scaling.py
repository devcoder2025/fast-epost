from concurrent.futures import ThreadPoolExecutor
import asyncio

class AILoadBalancer:
    def __init__(self, num_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=num_workers)
        self.workers = [ProductionAI() for _ in range(num_workers)]
        self.current_worker = 0
        
    async def process_request(self, text: str):
        worker = self.workers[self.current_worker]
        self.current_worker = (self.current_worker + 1) % len(self.workers)
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            worker.process_batch,
            [text]
        )
