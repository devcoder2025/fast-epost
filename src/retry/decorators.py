from functools import wraps
from typing import Optional
from .mechanism import RetryManager, RetryPolicy

def retry(
    max_attempts: Optional[int] = None,
    initial_delay: Optional[float] = None,
    max_delay: Optional[float] = None
):
    def decorator(func):
        policy = RetryPolicy()
        if max_attempts is not None:
            policy.max_attempts = max_attempts
        if initial_delay is not None:
            policy.initial_delay = initial_delay
        if max_delay is not None:
            policy.max_delay = max_delay
            
        retry_manager = RetryManager(policy)
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await retry_manager.execute(func, *args, **kwargs)
        return wrapper
    return decorator

# Direct usage
retry_manager = RetryManager()
result = await retry_manager.execute(your_async_function, arg1, arg2)

# Decorator usage
@retry(max_attempts=5)
async def fetch_data():
    # Your code here


