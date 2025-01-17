
import pytest
import asyncio
from src.circuit.breaker import CircuitBreaker, CircuitBreakerError
from src.circuit.state import CircuitState

@pytest.fixture
def circuit_breaker():
    return CircuitBreaker(
        failure_threshold=2,
        recovery_timeout=0.1,
        half_open_max_calls=2
    )

async def success_func():
    return "success"

async def failing_func():
    raise ValueError("Simulated failure")

@pytest.mark.asyncio
async def test_success_calls(circuit_breaker):
    wrapped = circuit_breaker(success_func)
    result = await wrapped()
    assert result == "success"
    assert circuit_breaker.state == CircuitState.CLOSED

@pytest.mark.asyncio
async def test_circuit_opens(circuit_breaker):
    wrapped = circuit_breaker(failing_func)
    
    # First failure
    with pytest.raises(ValueError):
        await wrapped()
    assert circuit_breaker.state == CircuitState.CLOSED
    
    # Second failure - should trip circuit
    with pytest.raises(ValueError):
        await wrapped()
    assert circuit_breaker.state == CircuitState.OPEN

@pytest.mark.asyncio
async def test_circuit_recovery(circuit_breaker):
    wrapped = circuit_breaker(success_func)
    
    # Trip the circuit
    circuit_breaker.state_manager.trip()
    assert circuit_breaker.state == CircuitState.OPEN
    
    # Wait for recovery timeout
    await asyncio.sleep(0.2)
    
    # Should move to half-open and allow calls
    result = await wrapped()
    assert result == "success"
    assert circuit_breaker.state == CircuitState.HALF_OPEN

@pytest.mark.asyncio
async def test_excluded_exceptions(circuit_breaker):
    breaker = CircuitBreaker(
        failure_threshold=2,
        excluded_exceptions=(ValueError,)
    )
    
    @breaker
    async def func():
        raise ValueError("Expected error")
    
    # Should not count towards failure threshold
    with pytest.raises(ValueError):
        await func()
    assert breaker.state == CircuitState.CLOSED

@pytest.mark.asyncio
async def test_half_open_to_closed(circuit_breaker):
    wrapped = circuit_breaker(success_func)
    
    # Set to half-open state
    circuit_breaker.state_manager.state = CircuitState.HALF_OPEN
    
    # Successful calls should reset to closed
    for _ in range(2):
        await wrapped()
    
    assert circuit_breaker.state == CircuitState.CLOSED
