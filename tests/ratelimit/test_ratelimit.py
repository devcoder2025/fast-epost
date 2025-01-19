import pytest
import asyncio
from src.ratelimit.limiter import RateLimiter, RateLimitExceeded
from src.ratelimit.strategies import (
    FixedWindowStrategy,
    SlidingWindowStrategy,
    RedisRateLimitStrategy
)

@pytest.fixture
def rate_limiter():
    return RateLimiter(
        strategy=FixedWindowStrategy(),
        limit=3,
        window=1
    )

@pytest.mark.asyncio
async def test_fixed_window_strategy():
    limiter = RateLimiter(
        strategy=FixedWindowStrategy(),
        limit=2,
        window=1
    )
    
    # First two requests should succeed
    result1 = await limiter.check_rate_limit("test")
    assert result1.allowed is True
    assert result1.remaining == 1
    
    result2 = await limiter.check_rate_limit("test")
    assert result2.allowed is True
    assert result2.remaining == 0
    
    # Third request should be blocked
    result3 = await limiter.check_rate_limit("test")
    assert result3.allowed is False
    assert result3.remaining == 0

@pytest.mark.asyncio
async def test_sliding_window_strategy():
    limiter = RateLimiter(
        strategy=SlidingWindowStrategy(),
        limit=2,
        window=1
    )
    
    result1 = await limiter.check_rate_limit("test")
    assert result1.allowed is True
    
    result2 = await limiter.check_rate_limit("test")
    assert result2.allowed is True
    
    result3 = await limiter.check_rate_limit("test")
    assert result3.allowed is False

@pytest.mark.asyncio
async def test_rate_limit_decorator(rate_limiter):
    call_count = 0
    
    @rate_limiter.rate_limit()
    async def test_func():
        nonlocal call_count
        call_count += 1
        return "success"
    
    # First three calls should succeed
    await test_func()
    await test_func()
    await test_func()
    
    # Fourth call should raise RateLimitExceeded
    with pytest.raises(RateLimitExceeded):
        await test_func()
    
    assert call_count == 3

@pytest.mark.asyncio
async def test_custom_key_function(rate_limiter):
    def custom_key(*args, **kwargs):
        return f"user:{kwargs.get('user_id')}"
    
    @rate_limiter.rate_limit(key_func=custom_key)
    async def test_func(user_id):
        return "success"
    
    # Different users should have separate limits
    await test_func(user_id="user1")
    await test_func(user_id="user2")
    await test_func(user_id="user1")
    await test_func(user_id="user2")
    
    # Third request for same user should fail
    with pytest.raises(RateLimitExceeded):
        await test_func(user_id="user1")
