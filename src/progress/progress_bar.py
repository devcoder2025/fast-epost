import sys
import time
from typing import Optional, Callable, Any, TypeVar, Generic, Iterable
from enum import Enum
from dataclasses import dataclass

T = TypeVar('T')

class ColorScheme(Enum):
    DEFAULT = '\033[0m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    INFO = '\033[94m'

@dataclass
class ProgressBarStyle:
    fill_char: str = "█"
    empty_char: str = "░"
    border_left: str = "|"
    border_right: str = "|"
    spinner_chars: tuple = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")

class ProgressBar(Generic[T]):
    def __init__(
        self,
        iterable: Optional[Iterable[T]] = None,
        total: Optional[int] = None,
        style: Optional[ProgressBarStyle] = None,
        width: int = 40,
        color_scheme: ColorScheme = ColorScheme.DEFAULT,
        description: str = "",
        unit: str = "it",
        dynamic_ncols: bool = False,
        show_speed: bool = True,
        refresh_rate: float = 0.1
    ):
        self.iterable = iterable
        self.total = len(iterable) if iterable is not None and total is None else total
        self.style = style or ProgressBarStyle()
        self.width = width
        self.color_scheme = color_scheme
        self.description = description
        self.unit = unit
        self.dynamic_ncols = dynamic_ncols
        self.show_speed = show_speed
        self.refresh_rate = refresh_rate
        
        self.n = 0
        self.start_time = time.time()
        self.last_print_time = 0
        self._last_line = ""
        
    def update(self, n: int = 1) -> None:
        self.n += n
        if time.time() - self.last_print_time > self.refresh_rate:
            self.refresh()
            
    def refresh(self) -> None:
        if self.total:
            percentage = self.n / float(self.total)
            filled_length = int(self.width * percentage)
            bar = (
                f"{self.style.fill_char * filled_length}"
                f"{self.style.empty_char * (self.width - filled_length)}"
            )
            
            elapsed_time = time.time() - self.start_time
            speed = self.n / elapsed_time if elapsed_time > 0 else 0
            
            line = (
                f"\r{self.color_scheme.value}"
                f"{self.description}: "
                f"{self.style.border_left}{bar}{self.style.border_right} "
                f"{percentage:>3.0%} "
                f"[{self.n}/{self.total} {self.unit}]"
            )
            
            if self.show_speed:
                line += f" ({speed:.2f} {self.unit}/s)"
                
            line += ColorScheme.DEFAULT.value
            
            if line != self._last_line:
                sys.stdout.write(line)
                sys.stdout.flush()
                self._last_line = line
                self.last_print_time = time.time()
                
    def __iter__(self):
        if self.iterable is None:
            raise TypeError("ProgressBar requires an iterable when used in a for loop")
        
        for obj in self.iterable:
            yield obj
            self.update()
            
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.refresh()
        sys.stdout.write('\n')
        sys.stdout.flush()
