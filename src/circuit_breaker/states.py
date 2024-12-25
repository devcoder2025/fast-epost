
from enum import Enum
import time
from typing import Optional, Callable
from dataclasses import dataclass

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitStats:
    total_requests: int = 0
    failed_requests: int = 0
    successful_requests: int = 0
    last_failure_time: Optional[float] = None
    last_success_time: Optional[float] = None

class CircuitStateHandler:
    def __init__(
        self,
        failure_threshold: int,
        recovery_timeout: float,
        success_threshold: int,
        on_state_change: Optional[Callable] = None
    ):
        self.state = CircuitState.CLOSED
        self.stats = CircuitStats()
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.half_open_successes = 0
        self.on_state_change = on_state_change

    def record_success(self):
        self.stats.total_requests += 1
        self.stats.successful_requests += 1
        self.stats.last_success_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            self.half_open_successes += 1
            if self.half_open_successes >= self.success_threshold:
                self._transition_to(CircuitState.CLOSED)

    def record_failure(self):
        self.stats.total_requests += 1
        self.stats.failed_requests += 1
        self.stats.last_failure_time = time.time()

        if self.state == CircuitState.CLOSED:
            failure_rate = self.stats.failed_requests / self.stats.total_requests
            if failure_rate >= self.failure_threshold:
                self._transition_to(CircuitState.OPEN)
        elif self.state == CircuitState.HALF_OPEN:
            self._transition_to(CircuitState.OPEN)

    def can_execute(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        elif self.state == CircuitState.OPEN:
            if time.time() - self.stats.last_failure_time >= self.recovery_timeout:
                self._transition_to(CircuitState.HALF_OPEN)
                return True
            return False
        else:  # HALF_OPEN
            return True

    def _transition_to(self, new_state: CircuitState):
        if new_state != self.state:
            old_state = self.state
            self.state = new_state
            
            if new_state == CircuitState.CLOSED:
                self.stats = CircuitStats()
            elif new_state == CircuitState.HALF_OPEN:
                self.half_open_successes = 0

            if self.on_state_change:
                self.on_state_change(old_state, new_state)
