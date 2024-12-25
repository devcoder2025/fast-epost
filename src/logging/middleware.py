from functools import wraps
import uuid
from .core import request_id

def request_logger_middleware():
    async def middleware(request, call_next):
        request_id.set(str(uuid.uuid4()))
        response = await call_next(request)
        return response
    return middleware

def log_execution_time():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger = StructuredLogger(__name__)
            logger.info(
                f"Function {func.__name__} executed",
                execution_time=execution_time,
                function=func.__name__
            )
            return result
        return wrapper
    return decorator
