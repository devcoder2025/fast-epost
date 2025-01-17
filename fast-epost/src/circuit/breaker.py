class CircuitBreakerError(Exception):
    """Exception raised when the circuit is open."""
    pass

class CircuitState:
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreaker:
    def __init__(self, failure_threshold, recovery_timeout, half_open_max_calls):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.state = CircuitState.CLOSED
        self.failure_count = 0

    def trip(self):
        self.state = CircuitState.OPEN

    def reset(self):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
