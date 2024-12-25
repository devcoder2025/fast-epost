from dataclasses import dataclass
from typing import Optional

@dataclass
class CacheConfig:
    max_size_bytes: int = 1024 * 1024 * 100  # 100MB default
    max_age_days: int = 30
    cleanup_threshold: float = 0.9  # 90% full triggers cleanup
    memory_limit_mb: int = 512
    enable_stats: bool = True
    compression_enabled: bool = False

class CacheStats:
    def __init__(self):
        self.hits: int = 0
        self.misses: int = 0
        self.evictions: int = 0
        self.total_items: int = 0
        self.total_size: int = 0
