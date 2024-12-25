from dataclasses import dataclass
from typing import Any, Dict, List
import re

class DataValidator:
    def __init__(self):
        self.rules = {}
        
    def add_rule(self, field: str, rule: callable):
        self.rules[field] = rule
        
    def validate(self, data: Dict[str, Any]) -> List[str]:
        errors = []
        for field, rule in self.rules.items():
            if not rule(data.get(field)):
                errors.append(f"Validation failed for {field}")
        return errors
