import aiofiles
import asyncio
from typing import List, Dict
import os
import logging

class AsyncFileHandler:
    async def read_file(self, file_path: str) -> str:
        try:
            async with aiofiles.open(file_path, mode='r') as f:
                content = await f.read()
            return content
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")
            return ""

    async def write_file(self, file_path: str, content: str) -> None:
        try:
            if not file_path.endswith('.txt'):  # Example validation for file type
                raise ValueError("Only .txt files are supported.")
            async with aiofiles.open(file_path, mode='w') as f:
                await f.write(content)
        except Exception as e:
            logging.error(f"Error writing to file {file_path}: {e}")
