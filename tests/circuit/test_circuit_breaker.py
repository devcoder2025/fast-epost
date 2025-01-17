import pytest
import asyncio
from src.circuit_breaker.breaker import (
    CircuitBreaker,
    CircuitBreakerRegistry,
    CircuitOpenError
)
from src.circuit_breaker.states import CircuitState

@pytest.fixture
def circuit_breaker():
    return CircuitBreaker(
        failure_threshold=0.5,
        recovery_timeout=0.1,
        success_threshold=2
    )

@pytest.mark.asyncio
async def test_successful_execution(circuit_breaker):
    @circuit_breaker
    async def success_func():
        return "success"

    result = await success_func()
    assert result == "success"
    assert circuit_breaker.state == CircuitState.CLOSED
    assert circuit_breaker.stats.successful_requests == 1

@pytest.mark.asyncio
async def test_circuit_opens_on_failures(circuit_breaker):
    failure_count = 0
    
    @circuit_breaker
    async def failing_func():
        nonlocal failure_count
        failure_count += 1
        raise ValueError("Simulated failure")

    # Generate failures
    for _ in range(3):
        with pytest.raises(ValueError):
            await failing_func()

    assert circuit_breaker.state == CircuitState.OPEN
    assert circuit_breaker.stats.failed_requests == 3

    # Circuit is open, should raise CircuitOpenError
    with pytest.raises(CircuitOpenError):
        await failing_func()

@pytest.mark.asyncio
async def test_half_open_state(circuit_breaker):
    @circuit_breaker
    async def failing_func():
        raise ValueError("Simulated failure")

    # Generate failures to open circuit
    for _ in range(3):
        with pytest.raises(ValueError):
            await failing_func()

    assert circuit_breaker.state == CircuitState.OPEN

    # Wait for recovery timeout
    await asyncio.sleep(0.2)

    # Circuit should now be half-open
    assert circuit_breaker.state_handler.can_execute()
    assert circuit_breaker.state == CircuitState.HALF_OPEN

@pytest.mark.asyncio
async def test_circuit_breaker_registry():
    registry = CircuitBreakerRegistry()
    
    # Get or create new circuit breaker
    breaker1 = registry.get_or_create("service1")
    breaker2 = registry.get_or_create("service2")
    
    assert breaker1 != breaker2
    assert registry.get("service1") == breaker1
    
    # Reset breaker
    registry.reset("service1")
    assert registry.get("service1") is None

@pytest.mark.asyncio
async def test_excluded_exceptions(circuit_breaker):
    circuit_breaker.excluded_exceptions = (ValueError,)
    
    @circuit_breaker
    async def func():
        raise ValueError("Excluded exception")

    # These errors should not count towards failure threshold
    for _ in range(5):
        with pytest.raises(ValueError):
            await func()

    assert circuit_breaker.state == CircuitState.CLOSED
