from typing import Dict, Any

class Settings:
    PERFORMANCE_SETTINGS: Dict[str, Any] = {
        'CACHE_ENABLED': True,
        'ASYNC_BATCH_SIZE': 100,
        'MAX_CONCURRENT_OPS': 5,
        'TEMPLATE_CACHE_SIZE': 1000,
        'MONITORING_ENABLED': True
    }
    
    @classmethod
    def get_setting(cls, key: str) -> Any:
        return cls.PERFORMANCE_SETTINGS.get(key)
