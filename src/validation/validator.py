
from typing import Dict, List, Any, Optional, Type
from .rules import ValidationRule, ValidationError

class Validator:
    def __init__(self):
        self.rules: Dict[str, List[ValidationRule]] = {}
        self.custom_validators: Dict[str, List[callable]] = {}

    def add_rule(self, field: str, rule: ValidationRule):
        if field not in self.rules:
            self.rules[field] = []
        self.rules[field].append(rule)

    def add_custom_validator(self, field: str, validator: callable):
        if field not in self.custom_validators:
            self.custom_validators[field] = []
        self.custom_validators[field].append(validator)

    async def validate(self, data: Dict[str, Any]) -> List[ValidationError]:
        errors: List[ValidationError] = []

        # Validate using rules
        for field, rules in self.rules.items():
            value = data.get(field)
            for rule in rules:
                error = await rule.validate(value, field)
                if error:
                    errors.append(error)

        # Run custom validators
        for field, validators in self.custom_validators.items():
            value = data.get(field)
            for validator in validators:
                try:
                    result = await validator(value, data)
                    if isinstance(result, ValidationError):
                        errors.append(result)
                    elif isinstance(result, list):
                        errors.extend([e for e in result if isinstance(e, ValidationError)])
                except Exception as e:
                    errors.append(
                        ValidationError(field, str(e), "custom_validation_error")
                    )

        return errors

    def validate_field(self, field: str, value: Any) -> List[ValidationError]:
        errors = []
        if field in self.rules:
            for rule in self.rules[field]:
                error = rule.validate(value, field)
                if error:
                    errors.append(error)
        return errors

class ValidatorBuilder:
    def __init__(self):
        self.validator = Validator()

    def required(self, field: str, message: str = None):
        from .rules import Required
        self.validator.add_rule(field, Required(message))
        return self

    def length(self, field: str, min: int = None, max: int = None, message: str = None):
        from .rules import Length
        self.validator.add_rule(field, Length(min, max, message))
        return self

    def pattern(self, field: str, pattern: str, message: str = None):
        from .rules import Pattern
        self.validator.add_rule(field, Pattern(pattern, message))
        return self

    def range(self, field: str, min_value=None, max_value=None, message: str = None):
        from .rules import Range
        self.validator.add_rule(field, Range(min_value, max_value, message))
        return self

    def custom(self, field: str, validator: callable):
        self.validator.add_custom_validator(field, validator)
        return self

    def build(self) -> Validator:
        return self.validator
