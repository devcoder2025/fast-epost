import os
import time
import shutil
import logging
from typing import Dict, Any, Optional, Tuple, List
import psutil
import zlib
from collections import OrderedDict
from threading import Lock

class Cache:
    """
    Enhanced cache implementation for managing file system resources
    with improved error handling and logging capabilities.
    """

    def __init__(self, base: str, config: Optional[CacheConfig] = None) -> None:
        self.config = config or CacheConfig()
        self.stats = CacheStats()
        self.logger = logging.getLogger(__name__)
        self.base = self._initialize_base_directory(base)
        self._validate_directory_permissions()
        
    def get_memory_usage(self) -> float:
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # MB
        
    def should_cleanup(self) -> bool:
        current_size = self.get_cache_size()
        return current_size > (self.config.max_size_bytes * self.config.cleanup_threshold)
        
    def compress_item(self, data: bytes) -> bytes:
        if self.config.compression_enabled:
            return zlib.compress(data)
        return data
        
    def decompress_item(self, data: bytes) -> bytes:
        if self.config.compression_enabled:
            return zlib.decompress(data)
        return data
        
    def _initialize_base_directory(self, base: str) -> str:
        if not os.path.isdir(base):
            os.makedirs(base, mode=0o700)
        return os.path.abspath(os.path.normpath(base))

    def _validate_directory_permissions(self) -> None:
        mode = os.stat(self.base).st_mode
        if (mode & 0o77) != 0:
            self.logger.warning(
                f"Security warning: Directory '{self.base}' has loose permissions: {mode:o}"
            )

    def clear(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        cleared_items = []
        failed_items = []
        
        for fn in os.listdir(self.base):
            full_path = os.path.join(self.base, fn)
            try:
                self._remove_cache_item(full_path)
                cleared_items.append(full_path)
                self.logger.debug(f"Successfully cleared cache item: {full_path}")
            except OSError as e:
                failed_items.append((full_path, str(e)))
                self.logger.error(f"Failed to clear cache item {full_path}: {e}")
        
        return cleared_items, failed_items

    def _remove_cache_item(self, path: str) -> None:
        if os.path.islink(path):
            os.unlink(path)
        elif os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    def get_cache_size(self) -> int:
        total_size = 0
        for dirpath, _, filenames in os.walk(self.base):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return total_size

    def cleanup_old_files(self, max_age_days: int = 30) -> List[str]:
        cutoff_time = time.time() - (max_age_days * 86400)
        removed = []
        
        for dirpath, _, filenames in os.walk(self.base):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    if os.path.getctime(fp) < cutoff_time:
                        os.remove(fp)
                        removed.append(fp)
                        self.logger.info(f"Removed old cache file: {fp}")
                except OSError as e:
                    self.logger.error(f"Failed to remove old cache file {fp}: {e}")
        
        return removed

class MemoryCache:
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self._cache: OrderedDict = OrderedDict()
        self._max_size = max_size
        self._ttl = ttl
        self._lock = Lock()
        self._stats = {'hits': 0, 'misses': 0}

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                self._stats['misses'] += 1
                return None
            
            value, timestamp = self._cache[key]
            if time.time() - timestamp > self._ttl:
                del self._cache[key]
                self._stats['misses'] += 1
                return None

            self._cache.move_to_end(key)
            self._stats['hits'] += 1
            return value

    def set(self, key: str, value: Any, compress: bool = False) -> None:
        with self._lock:
            if compress:
                value = zlib.compress(str(value).encode())
            
            if len(self._cache) >= self._max_size:
                self._cache.popitem(last=False)
            
            self._cache[key] = (value, time.time())
            self._cache.move_to_end(key)

class EnhancedCache:
    def __init__(self, base_path: str, memory_cache_size: int = 1000):
        self.disk_cache = DiskCache(base_path)
        self.memory_cache = MemoryCache(max_size=memory_cache_size)
        self._compression_threshold = 1024  # 1KB

    def get(self, key: str) -> Optional[Any]:
        # Try memory cache first
        value = self.memory_cache.get(key)
        if value is not None:
            return value

        # Fall back to disk cache
        value = self.disk_cache.get(key)
        if value is not None:
            self.memory_cache.set(key, value)
        return value

    def set(self, key: str, value: Any) -> None:
        # Determine if compression is needed
        should_compress = (
            isinstance(value, (str, bytes)) and 
            len(str(value)) > self._compression_threshold
        )
        
        self.memory_cache.set(key, value, compress=should_compress)
        self.disk_cache.set(key, value)

class DiskCache:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self._ensure_cache_dir()

    def _ensure_cache_dir(self) -> None:
        os.makedirs(self.base_path, exist_ok=True)
