
import pytest
import asyncio
from src.ratelimit.limiter import RateLimiter
from src.ratelimit.strategies import TokenBucket, SlidingWindow, FixedWindow

@pytest.fixture
def rate_limiter():
    return RateLimiter(
        strategy='token_bucket',
        rate=10,
        capacity=10
    )

@pytest.mark.asyncio
async def test_token_bucket():
    bucket = TokenBucket(rate=2, capacity=2)
    
    # First two requests should be allowed
    result1 = await bucket.acquire()
    result2 = await bucket.acquire()
    assert result1.allowed and result2.allowed
    
    # Third request should be denied
    result3 = await bucket.acquire()
    assert not result3.allowed

@pytest.mark.asyncio
async def test_sliding_window():
    window = SlidingWindow(max_requests=2, window_size=1)
    
    # First two requests should be allowed
    result1 = await window.acquire()
    result2 = await window.acquire()
    assert result1.allowed and result2.allowed
    
    # Third request should be denied
    result3 = await window.acquire()
    assert not result3.allowed

@pytest.mark.asyncio
async def test_fixed_window():
    window = FixedWindow(max_requests=2, window_size=1)
    
    # First two requests should be allowed
    result1 = await window.acquire()
    result2 = await window.acquire()
    assert result1.allowed and result2.allowed
    
    # Third request should be denied
    result3 = await window.acquire()
    assert not result3.allowed

@pytest.mark.asyncio
async def test_rate_limiter_acquire(rate_limiter):
    # Test multiple requests
    results = []
    for _ in range(12):
        result = await rate_limiter.acquire('test_key')
        results.append(result.allowed)
    
    # First 10 requests should be allowed, last 2 denied
    assert sum(results) == 10

@pytest.mark.asyncio
async def test_rate_limiter_namespaces(rate_limiter):
    # Test requests in different namespaces
    result1 = await rate_limiter.acquire('key', 'namespace1')
    result2 = await rate_limiter.acquire('key', 'namespace2')
    
    assert result1.allowed and result2.allowed

@pytest.mark.asyncio
async def test_rate_limiter_headers(rate_limiter):
    result = await rate_limiter.acquire('test_key')
    headers = rate_limiter.get_limit_headers(result)
    
    assert 'X-RateLimit-Limit' in headers
    assert 'X-RateLimit-Remaining' in headers
    assert 'X-RateLimit-Reset' in headers
