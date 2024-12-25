import pytest
import asyncio
from src.cache.manager import CacheManager, CachePattern
from src.cache.backends import MemoryCache, RedisCache

@pytest.fixture
async def cache_manager():
    manager = CacheManager(MemoryCache())
    yield manager
    await manager.clear()

@pytest.mark.asyncio
async def test_basic_cache_operations(cache_manager):
    # Test set and get
    await cache_manager.set("test_key", "test_value")
    value = await cache_manager.get("test_key")
    assert value == "test_value"
    
    # Test delete
    await cache_manager.delete("test_key")
    value = await cache_manager.get("test_key")
    assert value is None

@pytest.mark.asyncio
async def test_cache_ttl(cache_manager):
    await cache_manager.set("test_key", "test_value", ttl=1)
    value = await cache_manager.get("test_key")
    assert value == "test_value"
    
    await asyncio.sleep(1.1)
    value = await cache_manager.get("test_key")
    assert value is None

@pytest.mark.asyncio
async def test_cached_decorator(cache_manager):
    call_count = 0
    
    @cache_manager.cached(ttl=10)
    async def test_func(param):
        nonlocal call_count
        call_count += 1
        return f"result_{param}"
    
    # First call should execute the function
    result1 = await test_func("test")
    assert result1 == "result_test"
    assert call_count == 1
    
    # Second call should return cached result
    result2 = await test_func("test")
    assert result2 == "result_test"
    assert call_count == 1

@pytest.mark.asyncio
async def test_cache_aside_pattern(cache_manager):
    call_count = 0
    
    @CachePattern.cache_aside(cache_manager, ttl=10)
    async def get_data(key):
        nonlocal call_count
        call_count += 1
        return f"data_{key}"
    
    # First call
    result1 = await get_data("test")
    assert result1 == "data_test"
    assert call_count == 1
    
    # Cached call
    result2 = await get_data("test")
    assert result2 == "data_test"
    assert call_count == 1

@pytest.mark.asyncio
async def test_write_through_pattern(cache_manager):
    @CachePattern.write_through(cache_manager, ttl=10)
    async def save_data(key, value):
        return value
    
    await save_data("test", "test_value")
    cached_value = await cache_manager.get("save_data:(('test', 'test_value'),):{}")
    assert cached_value == "test_value"
