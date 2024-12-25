
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
import re
from datetime import datetime

@dataclass
class ValidationError:
    field: str
    message: str
    code: str

class ValidationRule:
    def __init__(self, message: Optional[str] = None):
        self.message = message

    async def validate(self, value: Any, field_name: str) -> Optional[ValidationError]:
        raise NotImplementedError

class Required(ValidationRule):
    def __init__(self, message: str = "Field is required"):
        super().__init__(message)

    async def validate(self, value: Any, field_name: str) -> Optional[ValidationError]:
        if value is None or (isinstance(value, str) and not value.strip()):
            return ValidationError(field_name, self.message, "required")
        return None

class Length(ValidationRule):
    def __init__(self, min: int = None, max: int = None, message: str = None):
        super().__init__(message)
        self.min = min
        self.max = max

    async def validate(self, value: Any, field_name: str) -> Optional[ValidationError]:
        if value is None:
            return None

        length = len(str(value))
        if self.min and length < self.min:
            return ValidationError(
                field_name,
                self.message or f"Minimum length is {self.min}",
                "min_length"
            )
        if self.max and length > self.max:
            return ValidationError(
                field_name,
                self.message or f"Maximum length is {self.max}",
                "max_length"
            )
        return None

class Pattern(ValidationRule):
    def __init__(self, pattern: str, message: str = "Invalid format"):
        super().__init__(message)
        self.pattern = re.compile(pattern)

    async def validate(self, value: Any, field_name: str) -> Optional[ValidationError]:
        if value is None:
            return None
        if not self.pattern.match(str(value)):
            return ValidationError(field_name, self.message, "pattern")
        return None

class Range(ValidationRule):
    def __init__(
        self,
        min_value: Union[int, float, datetime] = None,
        max_value: Union[int, float, datetime] = None,
        message: str = None
    ):
        super().__init__(message)
        self.min_value = min_value
        self.max_value = max_value

    async def validate(self, value: Any, field_name: str) -> Optional[ValidationError]:
        if value is None:
            return None

        if self.min_value and value < self.min_value:
            return ValidationError(
                field_name,
                self.message or f"Minimum value is {self.min_value}",
                "min_value"
            )
        if self.max_value and value > self.max_value:
            return ValidationError(
                field_name,
                self.message or f"Maximum value is {self.max_value}",
                "max_value"
            )
        return None
