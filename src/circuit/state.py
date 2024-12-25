
from enum import Enum
from dataclasses import dataclass
import time
from typing import Optional, Callable, Any

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open" 
    HALF_OPEN = "half_open"

@dataclass
class CircuitStats:
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[float] = None
    last_success_time: Optional[float] = None
    total_requests: int = 0

class CircuitStateManager:
    def __init__(
        self,
        failure_threshold: int,
        recovery_timeout: float,
        half_open_max_calls: int = 3
    ):
        self.state = CircuitState.CLOSED
        self.stats = CircuitStats()
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.last_state_change = time.time()

    def record_success(self):
        self.stats.success_count += 1
        self.stats.total_requests += 1
        self.stats.last_success_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            if self.stats.success_count >= self.half_open_max_calls:
                self.reset()

    def record_failure(self):
        self.stats.failure_count += 1
        self.stats.total_requests += 1
        self.stats.last_failure_time = time.time()

        if self.state == CircuitState.CLOSED:
            if self.stats.failure_count >= self.failure_threshold:
                self.trip()
        elif self.state == CircuitState.HALF_OPEN:
            self.trip()

    def reset(self):
        self.state = CircuitState.CLOSED
        self.stats = CircuitStats()
        self.last_state_change = time.time()

    def trip(self):
        self.state = CircuitState.OPEN
        self.last_state_change = time.time()

    def attempt_reset(self) -> bool:
        if (self.state == CircuitState.OPEN and
            time.time() - self.last_state_change >= self.recovery_timeout):
            self.state = CircuitState.HALF_OPEN
            self.stats.failure_count = 0
            self.stats.success_count = 0
            self.last_state_change = time.time()
            return True
        return False
