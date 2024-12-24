from dataclasses import dataclass
from typing import List, Dict
import asyncio

@dataclass
class BatchJob:
    files: List[str]
    destination: str
    
class BatchProcessor:
    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.file_handler = AsyncFileHandler()
        
    async def process_batch(self, batch: BatchJob) -> Dict[str, bool]:
        results = {}
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def process_file(file_path: str):
            async with semaphore:
                try:
                    await self.file_handler.read_file(file_path)
                    results[file_path] = True
                except Exception:
                    results[file_path] = False
                    
        tasks = [process_file(f) for f in batch.files]
        await asyncio.gather(*tasks)
        return results
