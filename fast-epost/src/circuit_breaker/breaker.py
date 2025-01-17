class CircuitOpenError(Exception):
    """Exception raised when the circuit is open."""
    pass

class CircuitState:
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreaker:
    def __init__(self, failure_threshold, recovery_timeout, success_threshold):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0

    def trip(self):
        self.state = CircuitState.OPEN

    def reset(self):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0

class CircuitBreakerRegistry:
    def __init__(self):
        self.breakers = {}

    def get_or_create(self, name):
        if name not in self.breakers:
            self.breakers[name] = CircuitBreaker(0.5, 1, 2)
        return self.breakers[name]

    def reset(self, name):
        if name in self.breakers:
            self.breakers[name].reset()
            del self.breakers[name]
