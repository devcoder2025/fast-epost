import asyncio
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import List, Set, Dict, Optional, Any
from urllib.parse import urlparse
import aiohttp
import logging

@dataclass
class CollectorConfig:
    max_concurrent_requests: int = 10
    timeout_seconds: int = 30
    max_retries: int = 3
    chunk_size: int = 1024
    verify_ssl: bool = True

class AsyncLinkCollector:
    def __init__(self, config: Optional[CollectorConfig] = None):
        self.config = config or CollectorConfig()
        self.logger = logging.getLogger(__name__)
        self.collected_links: Set[str] = set()
        self.session: Optional[aiohttp.ClientSession] = None
        self._executor = ThreadPoolExecutor(max_workers=self.config.max_concurrent_requests)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
        self._executor.shutdown()

    async def collect_links(self, urls: List[str]) -> Dict[str, Set[str]]:
        if not self.session:
            raise RuntimeError("Session not initialized. Use async with context.")
        
        tasks = [self.process_url(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            url: links for url, links in zip(urls, results)
            if isinstance(links, set)
        }

    async def process_url(self, url: str) -> Set[str]:
        for attempt in range(self.config.max_retries):
            try:
                async with self.session.get(
                    url,
                    timeout=self.config.timeout_seconds,
                    ssl=self.config.verify_ssl
                ) as response:
                    content = await response.text()
                    return await self._extract_links(content, url)
            except Exception as e:
                self.logger.error(f"Error processing {url} (attempt {attempt + 1}): {e}")
                if attempt == self.config.max_retries - 1:
                    raise

    async def _extract_links(self, content: str, base_url: str) -> Set[str]:
        def extract_worker(content: str) -> Set[str]:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            return {a.get('href') for a in soup.find_all('a', href=True)}

        loop = asyncio.get_event_loop()
        links = await loop.run_in_executor(
            self._executor,
            extract_worker,
            content
        )
        
        return {self._normalize_url(link, base_url) for link in links}

    def _normalize_url(self, url: str, base_url: str) -> str:
        parsed = urlparse(url)
        base_parsed = urlparse(base_url)
        
        if not parsed.netloc:
            return f"{base_parsed.scheme}://{base_parsed.netloc}{parsed.path}"
        return url
