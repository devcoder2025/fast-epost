
from .auth import JWTAuth
from .rate_limiter import RateLimiter
from .audit import AuditLogger

class SecurityManager:
    def __init__(self, secret_key: str):
        self.auth = JWTAuth(secret_key)
        self.rate_limiter = RateLimiter()
        self.audit = AuditLogger()

    def secure_endpoint(self, f):
        @self.rate_limiter.limiter
        @self.auth.token_required
        def wrapped(*args, **kwargs):
            result = f(*args, **kwargs)
            self.audit.log_event(
                event_type=f.__name__,
                user_id=self.auth.get_current_user(),
                data={'endpoint': f.__name__}
            )
            return result
        return wrapped
