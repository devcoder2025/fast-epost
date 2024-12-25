from functools import wraps
from flask import request, abort
from typing import Dict, Any, Callable

class APIVersionManager:
    def __init__(self):
        self.versions: Dict[str, Dict[str, Callable]] = {}
        
    def route(self, version: str):
        def decorator(f: Callable):
            if version not in self.versions:
                self.versions[version] = {}
            self.versions[version][f.__name__] = f
            
            @wraps(f)
            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapped
        return decorator
