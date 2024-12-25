import time
import resource
from typing import Dict, List, Optional, Set
import threading
from datetime import datetime
import operator
from dataclasses import dataclass

@dataclass
class SecurityPolicy:
    version: str
    max_requests_per_minute: int = 60
    max_memory_mb: int = 512
    max_cpu_time: int = 30
    allowed_modules: Set[str] = None
    allowed_attributes: Set[str] = None
    
    def __post_init__(self):
        self.allowed_modules = self.allowed_modules or {'math', 'datetime'}
        self.allowed_attributes = self.allowed_attributes or {'upper', 'lower', 'strip'}

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self._lock = threading.Lock()
        
    def is_allowed(self) -> bool:
        with self._lock:
            now = time.time()
            self.requests = [req for req in self.requests if now - req < self.time_window]
            
            if len(self.requests) >= self.max_requests:
                return False
                
            self.requests.append(now)
            return True

class ResourceMonitor:
    def __init__(self, max_memory_mb: int, max_cpu_time: int):
        self.max_memory_mb = max_memory_mb
        self.max_cpu_time = max_cpu_time
        self.start_time = time.time()
        
    def check_limits(self) -> Optional[str]:
        # Check memory usage
        memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
        if memory_usage > self.max_memory_mb:
            return f"Memory limit exceeded: {memory_usage:.1f}MB > {self.max_memory_mb}MB"
            
        # Check CPU time
        cpu_time = time.time() - self.start_time
        if cpu_time > self.max_cpu_time:
            return f"CPU time limit exceeded: {cpu_time:.1f}s > {self.max_cpu_time}s"
            
        return None

class EnhancedSandbox:
    def __init__(self, policy: SecurityPolicy):
        self.policy = policy
        self.rate_limiter = RateLimiter(policy.max_requests_per_minute)
        self.resource_monitor = ResourceMonitor(
            policy.max_memory_mb,
            policy.max_cpu_time
        )
        self._execution_history: List[Dict] = []
        
    def execute(self, code: str, globals_dict: Dict = None) -> Any:
        if not self.rate_limiter.is_allowed():
            raise SecurityError("Rate limit exceeded")
            
        if resource_violation := self.resource_monitor.check_limits():
            raise SecurityError(f"Resource limit violated: {resource_violation}")
            
        try:
            self._validate_code(code)
            result = self._execute_safely(code, globals_dict or {})
            self._log_execution(code, result)
            return result
        except Exception as e:
            self._log_execution(code, error=str(e))
            raise
            
    def _validate_code(self, code: str) -> None:
        import ast
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        if name.name not in self.policy.allowed_modules:
                            raise SecurityError(f"Import not allowed: {name.name}")
        except SyntaxError as e:
            raise SecurityError(f"Invalid syntax: {e}")
            
    def _execute_safely(self, code: str, globals_dict: Dict) -> Any:
        locals_dict = {}
        return exec(code, globals_dict, locals_dict)
        
    def _log_execution(self, code: str, result: Any = None, error: str = None) -> None:
        self._execution_history.append({
            'timestamp': datetime.now().isoformat(),
            'code': code,
            'result': str(result) if result is not None else None,
            'error': error,
            'policy_version': self.policy.version
        })
        
    def get_execution_history(self) -> List[Dict]:
        return self._execution_history.copy()

class SecurityError(Exception):
    pass
