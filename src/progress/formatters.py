from typing import Callable, Any
from datetime import timedelta

def format_time(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))

def format_bytes(num: float) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f"{num:3.1f} {unit}"
        num /= 1024.0
    return f"{num:.1f} PB"

class ProgressFormatter:
    @staticmethod
    def percentage(progress: float) -> str:
        return f"{progress:.1%}"
    
    @staticmethod
    def fraction(current: int, total: int) -> str:
        return f"{current}/{total}"
    
    @staticmethod
    def speed(items: int, seconds: float, unit: str = "it") -> str:
        speed = items / seconds if seconds > 0 else 0
        return f"{speed:.2f} {unit}/s"
