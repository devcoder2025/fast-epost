import asyncio
import aiohttp
from typing import List, Dict, Set, Optional
from dataclasses import dataclass
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from src.cache.cache import EnhancedCache

@dataclass
class CollectorConfig:
    max_connections: int = 10
    request_timeout: int = 30
    max_queue_size: int = 1000
    cache_ttl: int = 3600
    retry_attempts: int = 3
    verify_ssl: bool = True

class AsyncLinkCollector:
    def __init__(
        self,
        config: Optional[CollectorConfig] = None,
        cache_dir: str = ".cache"
    ):
        self.config = config or CollectorConfig()
        self.cache = EnhancedCache(cache_dir)
        self.session: Optional[aiohttp.ClientSession] = None
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=self.config.max_queue_size)
        self.semaphore = asyncio.Semaphore(self.config.max_connections)
        self.collected_links: Dict[str, Set[str]] = {}

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(
            limit=self.config.max_connections,
            verify_ssl=self.config.verify_ssl
        )
        self.session = aiohttp.ClientSession(connector=connector)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def collect_links(self, urls: List[str]) -> Dict[str, Set[str]]:
        workers = [
            asyncio.create_task(self._worker())
            for _ in range(self.config.max_connections)
        ]

        for url in urls:
            await self.queue.put(url)

        await self.queue.join()
        for worker in workers:
            worker.cancel()

        await asyncio.gather(*workers, return_exceptions=True)
        return self.collected_links

    async def _worker(self):
        while True:
            try:
                url = await self.queue.get()
                try:
                    links = await self._process_url(url)
                    self.collected_links[url] = links
                finally:
                    self.queue.task_done()
            except asyncio.CancelledError:
                break

    async def _process_url(self, url: str) -> Set[str]:
        cache_key = f"links:{url}"
        cached_links = self.cache.get(cache_key)
        if cached_links:
            return cached_links

        async with self.semaphore:
            for attempt in range(self.config.retry_attempts):
                try:
                    async with self.session.get(
                        url,
                        timeout=self.config.request_timeout
                    ) as response:
                        content = await response.text()
                        links = await self._extract_links(content, url)
                        self.cache.set(cache_key, links)
                        return links
                except Exception as e:
                    if attempt == self.config.retry_attempts - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)

    async def _extract_links(self, content: str, base_url: str) -> Set[str]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._parse_links,
            content,
            base_url
        )

    def _parse_links(self, content: str, base_url: str) -> Set[str]:
        soup = BeautifulSoup(content, 'html.parser')
        links = set()
        base_parsed = urlparse(base_url)

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            parsed = urlparse(href)
            if not parsed.netloc:
                href = f"{base_parsed.scheme}://{base_parsed.netloc}{parsed.path}"
            links.add(href)

        return links
