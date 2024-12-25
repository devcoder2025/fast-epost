import pytest
import asyncio
from unittest.mock import Mock, patch
from src.collector.link_collector import AsyncLinkCollector, CollectorConfig

@pytest.fixture
def collector():
    return AsyncLinkCollector(CollectorConfig(max_connections=2))

@pytest.mark.asyncio
async def test_collector_initialization(collector):
    assert collector.config.max_connections == 2
    assert collector.queue.maxsize == 1000

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
async def test_connection_pooling():
    config = CollectorConfig(max_connections=2)
    async with AsyncLinkCollector(config) as collector:
        urls = [f"https://example.com/{i}" for i in range(5)]
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = Mock()
            mock_response.text = asyncio.coroutine(lambda: "<html></html>")
            mock_get.return_value.__aenter__.return_value = mock_response
            
            results = await collector.collect_links(urls)
            assert len(results) == 5

@pytest.mark.asyncio
async def test_caching():
    async with AsyncLinkCollector() as collector:
        url = "https://example.com"
        mock_content = "<html><a href='https://example.com/1'>Link</a></html>"
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = Mock()
            mock_response.text = asyncio.coroutine(lambda: mock_content)
            mock_get.return_value.__aenter__.return_value = mock_response
            
            # First request
            result1 = await collector.collect_links([url])
            # Second request (should use cache)
            result2 = await collector.collect_links([url])
            
            assert result1 == result2
            assert mock_get.call_count == 1