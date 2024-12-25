import pytest
import time
from src.cache.cache import MemoryCache, EnhancedCache

def test_memory_cache_basic():
    cache = MemoryCache(max_size=2)
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    
    assert cache.get('key1') == 'value1'
    assert cache.get('key2') == 'value2'

def test_memory_cache_eviction():
    cache = MemoryCache(max_size=2)
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')
    
    assert cache.get('key1') is None
    assert cache.get('key2') == 'value2'
    assert cache.get('key3') == 'value3'

def test_memory_cache_ttl():
    cache = MemoryCache(max_size=2, ttl=1)
    cache.set('key1', 'value1')
    
    assert cache.get('key1') == 'value1'
    time.sleep(1.1)
    assert cache.get('key1') is None

def test_enhanced_cache_compression():
    cache = EnhancedCache('/tmp/cache')
    large_value = 'x' * 2000
    cache.set('large_key', large_value)
    
    assert cache.get('large_key') == large_value

def test_cache_stats():
    cache = MemoryCache()
    cache.set('key1', 'value1')
    
    cache.get('key1')  # Hit
    cache.get('key2')  # Miss
    
    assert cache._stats['hits'] == 1
    assert cache._stats['misses'] == 1
