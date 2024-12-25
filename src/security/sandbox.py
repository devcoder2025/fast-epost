import operator
from typing import Dict, Any, Callable, Set, Optional
from dataclasses import dataclass

@dataclass
class SecurityPolicy:
    allowed_builtins: Set[str]
    allowed_attributes: Set[str]
    allowed_modules: Set[str]
    max_recursion_depth: int = 100
    max_string_length: int = 10000

class SandboxedEnvironment:
    default_binop_table: Dict[str, Callable[[Any, Any], Any]] = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '//': operator.floordiv,
        '**': operator.pow,
        '%': operator.mod,
    }

    default_unop_table: Dict[str, Callable[[Any], Any]] = {
        '+': operator.pos,
        '-': operator.neg,
    }

    def __init__(self, policy: Optional[SecurityPolicy] = None):
        self.policy = policy or self._default_policy()
        self.binop_table = self.default_binop_table.copy()
        self.unop_table = self.default_unop_table.copy()
        self._recursion_depth = 0

    def _default_policy(self) -> SecurityPolicy:
        return SecurityPolicy(
            allowed_builtins={'len', 'str', 'int', 'float', 'bool'},
            allowed_attributes={'upper', 'lower', 'strip', 'split', 'join'},
            allowed_modules={'math', 'datetime'}
        )

    def call_binop(self, operator: str, left: Any, right: Any) -> Any:
        if operator not in self.binop_table:
            raise SecurityError(f"Operator '{operator}' not allowed")
        return self.binop_table[operator](left, right)

    def call_unop(self, operator: str, operand: Any) -> Any:
        if operator not in self.unop_table:
            raise SecurityError(f"Operator '{operator}' not allowed")
        return self.unop_table[operator](operand)

    def check_attribute_access(self, obj: Any, attribute: str) -> bool:
        if attribute not in self.policy.allowed_attributes:
            raise SecurityError(f"Attribute '{attribute}' access not allowed")
        return True

    def check_module_import(self, module_name: str) -> bool:
        if module_name not in self.policy.allowed_modules:
            raise SecurityError(f"Module '{module_name}' import not allowed")
        return True

class SecurityError(Exception):
    pass
