
from typing import Dict, Any, Optional
import threading

class ConfigStore:
    def __init__(self):
        self._store: Dict[str, Dict] = {}
        self._lock = threading.RLock()

    def get(self, namespace: str, key: str) -> Any:
        with self._lock:
            namespace_config = self._store.get(namespace, {})
            keys = key.split('.')
            value = namespace_config
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    return None
            return value

    def set(self, namespace: str, key: str, value: Any):
        with self._lock:
            if namespace not in self._store:
                self._store[namespace] = {}

            keys = key.split('.')
            current = self._store[namespace]
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            current[keys[-1]] = value

    def get_namespace(self, namespace: str) -> Optional[Dict]:
        with self._lock:
            return self._store.get(namespace)

    def set_namespace(self, namespace: str, config: Dict):
        with self._lock:
            self._store[namespace] = config

    def delete_namespace(self, namespace: str):
        with self._lock:
            if namespace in self._store:
                del self._store[namespace]
