import pytest
import asyncio
from unittest.mock import Mock, patch
from src.collector.link_collector import AsyncLinkCollector, CollectorConfig

@pytest.fixture
def collector():
    return AsyncLinkCollector(CollectorConfig(max_concurrent_requests=2))

@pytest.mark.asyncio
async def test_collector_initialization(collector):
    assert collector.config.max_concurrent_requests == 2
    assert collector.collected_links == set()

@pytest.mark.asyncio
async def test_url_normalization(collector):
    base_url = "https://example.com"
    relative_url = "/path"
    normalized = collector._normalize_url(relative_url, base_url)
    assert normalized == "https://example.com/path"

@pytest.mark.asyncio
async def test_link_collection():
    async with AsyncLinkCollector() as collector:
        mock_content = """
        <html>
            <body>
                <a href="https://example.com/1">Link 1</a>
                <a href="https://example.com/2">Link 2</a>
            </body>
        </html>
        """
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = Mock()
            mock_response.text = asyncio.coroutine(lambda: mock_content)
            mock_get.return_value.__aenter__.return_value = mock_response
            
            results = await collector.collect_links(["https://example.com"])
            assert len(results["https://example.com"]) == 2

@pytest.mark.asyncio
async def test_error_handling(collector):
    with pytest.raises(Exception):
        await collector.process_url("invalid-url")

@pytest.mark.asyncio
async def test_concurrent_collection():
    config = CollectorConfig(max_concurrent_requests=5)
    async with AsyncLinkCollector(config) as collector:
        urls = [f"https://example.com/{i}" for i in range(10)]
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = Mock()
            mock_response.text = asyncio.coroutine(lambda: "<html></html>")
            mock_get.return_value.__aenter__.return_value = mock_response
            
            results = await collector.collect_links(urls)
            assert len(results) == 10
