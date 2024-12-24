from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class AppError:
    code: str
    message: str
    details: Dict[str, Any]

class ErrorHandler:
    def __init__(self):
        self.error_registry = {}
        
    def register_error(self, code: str, handler: callable):
        self.error_registry[code] = handler
        
    def handle_error(self, error: AppError):
        if handler := self.error_registry.get(error.code):
            return handler(error)
