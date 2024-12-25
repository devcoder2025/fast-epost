import pytest
import asyncio
from src.cache.manager import CacheManager
from src.cache.backends import MemoryCache, RedisCache

@pytest.fixture
async def cache_manager():
    manager = CacheManager(backend='memory')
    await manager.start()
    yield manager
    await manager.stop()

@pytest.mark.asyncio
async def test_cache_set_get(cache_manager):
    await cache_manager.set('test_key', 'test_value')
    value = await cache_manager.get('test_key')
    assert value == 'test_value'

@pytest.mark.asyncio
async def test_cache_ttl():
    cache = MemoryCache()
    await cache.start()
    await cache.set('test_key', 'test_value', ttl=1)
    assert await cache.get('test_key') == 'test_value'
    await asyncio.sleep(1.1)
    assert await cache.get('test_key') is None
    await cache.stop()

@pytest.mark.asyncio
async def test_cache_delete(cache_manager):
    await cache_manager.set('test_key', 'test_value')
    await cache_manager.delete('test_key')
    assert await cache_manager.get('test_key') is None

@pytest.mark.asyncio
async def test_cache_clear(cache_manager):
    await cache_manager.set('key1', 'value1')
    await cache_manager.set('key2', 'value2')
    await cache_manager.clear()
    assert await cache_manager.get('key1') is None
    assert await cache_manager.get('key2') is None

@pytest.mark.asyncio
async def test_cache_increment(cache_manager):
    await cache_manager.set('counter', 0)
    value = await cache_manager.increment('counter')
    assert value == 1
    value = await cache_manager.increment('counter', 2)
    assert value == 3

@pytest.mark.asyncio
async def test_cache_get_or_set(cache_manager):
    async def default_value():
        return "computed_value"
    
    value = await cache_manager.get_or_set('missing_key', default_value)
    assert value == "computed_value"
    assert await cache_manager.get('missing_key') == "computed_value"
