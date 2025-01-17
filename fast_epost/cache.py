from functools import lru_cache
from typing import Optional
from typing import Optional
import asyncio
from pathlib import Path

class TemplateCache:
    # Add any new caching strategies or configurations here
    def __init__(self, cache_size: int = 100):
        self.cache = lru_cache(maxsize=cache_size)(self._load_template)
        
    def _load_template(self, template_path: str) -> str:
        with open(template_path) as f:
            return f.read()
            
    def get_template(self, template_path: str) -> str:
        return self.cache(template_path)
        
    def invalidate(self, template_path: Optional[str] = None):
        if template_path:
            self.cache.cache_clear()
