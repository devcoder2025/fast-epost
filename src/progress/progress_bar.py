import sys
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass
import psutil

@dataclass
class ProgressStats:
    start_time: float
    current: int
    total: int
    rate: float = 0.0
    eta_seconds: float = 0.0
    memory_usage_mb: float = 0.0
    is_paused: bool = False

class EnhancedProgressBar:
    def __init__(
        self,
        total: int,
        description: str = "",
        width: int = 40,
        show_memory: bool = True
    ):
        self.total = total
        self.description = description
        self.width = width
        self.show_memory = show_memory
        self._stats = ProgressStats(
            start_time=time.time(),
            current=0,
            total=total
        )
        self._last_update = 0
        self._update_interval = 0.1

    def update(self, n: int = 1) -> None:
        if self._stats.is_paused:
            return

        self._stats.current += n
        now = time.time()
        
        if now - self._last_update >= self._update_interval:
            self._update_stats()
            self._render()
            self._last_update = now

    def _update_stats(self) -> None:
        elapsed = time.time() - self._stats.start_time
        if elapsed > 0:
            self._stats.rate = self._stats.current / elapsed
            remaining = self.total - self._stats.current
            self._stats.eta_seconds = remaining / self._stats.rate if self._stats.rate > 0 else 0
        
        if self.show_memory:
            process = psutil.Process()
            self._stats.memory_usage_mb = process.memory_info().rss / (1024 * 1024)

    def _render(self) -> None:
        percentage = self._stats.current / self.total
        filled_width = int(self.width * percentage)
        
        bar = (
            "█" * filled_width +
            "░" * (self.width - filled_width)
        )
        
        eta = time.strftime("%H:%M:%S", time.gmtime(self._stats.eta_seconds))
        memory = f"Memory: {self._stats.memory_usage_mb:.1f}MB" if self.show_memory else ""
        
        status = (
            f"\r{self.description}: [{bar}] "
            f"{percentage:>3.0%} "
            f"({self._stats.current}/{self.total}) "
            f"Rate: {self._stats.rate:.1f}/s "
            f"ETA: {eta} {memory}"
        )
        
        sys.stdout.write(status)
        sys.stdout.flush()

    def pause(self) -> None:
        self._stats.is_paused = True

    def resume(self) -> None:
        self._stats.is_paused = False
        self._stats.start_time = time.time() - (
            self._stats.current / self._stats.rate if self._stats.rate > 0 else 0
        )

    def finish(self) -> None:
        self._stats.current = self.total
        self._update_stats()
        self._render()
        sys.stdout.write("\n")
        sys.stdout.flush()
