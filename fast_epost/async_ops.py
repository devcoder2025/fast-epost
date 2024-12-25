import aiofiles
import asyncio
from typing import List, Dict

class AsyncFileHandler:
    async def read_file(self, file_path: str) -> str:
        async with aiofiles.open(file_path, mode='r') as f:
            content = await f.read()
        return content
        
    async def write_file(self, file_path: str, content: str) -> None:
        async with aiofiles.open(file_path, mode='w') as f:
            await f.write(content)
