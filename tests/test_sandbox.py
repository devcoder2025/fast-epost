import pytest
import time
from src.security.sandbox import (
    EnhancedSandbox,
    SecurityPolicy,
    SecurityError,
    RateLimiter
)

@pytest.fixture
def sandbox():
    policy = SecurityPolicy(
        version="1.0",
        max_requests_per_minute=10,
        max_memory_mb=100,
        max_cpu_time=5
    )
    return EnhancedSandbox(policy)

def test_rate_limiting():
    limiter = RateLimiter(max_requests=2, time_window=1)
    assert limiter.is_allowed()
    assert limiter.is_allowed()
    assert not limiter.is_allowed()
    time.sleep(1)
    assert limiter.is_allowed()

def test_code_execution(sandbox):
    result = sandbox.execute("x = 1 + 1")
    assert result is None
    
    with pytest.raises(SecurityError):
        sandbox.execute("import os")

def test_resource_monitoring(sandbox):
    # Test memory limit
    with pytest.raises(SecurityError) as exc:
        sandbox.execute("x = ' ' * (1024 * 1024 * 200)")  # Allocate 200MB
    assert "Memory limit" in str(exc.value)
    
    # Test CPU time limit
    with pytest.raises(SecurityError) as exc:
        sandbox.execute("while True: pass")
    assert "CPU time limit" in str(exc.value)

def test_execution_history(sandbox):
    sandbox.execute("x = 42")
    history = sandbox.get_execution_history()
    assert len(history) == 1
    assert history[0]['code'] == "x = 42"
    assert history[0]['policy_version'] == "1.0"

def test_policy_validation():
    policy = SecurityPolicy(
        version="1.1",
        allowed_modules={'math'}
    )
    sandbox = EnhancedSandbox(policy)
    
    sandbox.execute("import math")
    with pytest.raises(SecurityError):
        sandbox.execute("import datetime")
