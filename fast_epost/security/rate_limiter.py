
from datetime import datetime, timedelta
from collections import defaultdict
import threading
from typing import Dict, List
from flask import request, jsonify

class RateLimiter:
    def __init__(self, limit: int = 60, window: int = 60):
        self.limit = limit  # requests per window
        self.window = window  # window in seconds
        self.requests: Dict[str, List[datetime]] = defaultdict(list)
        self._lock = threading.Lock()
    
    def is_allowed(self, client_id: str) -> bool:
        with self._lock:
            now = datetime.now()
            window_ago = now - timedelta(seconds=self.window)
            
            # Clean old requests
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id]
                if req_time > window_ago
            ]
            
            if len(self.requests[client_id]) >= self.limit:
                return False
                
            self.requests[client_id].append(now)
            return True

    def limiter(self, f):
        def decorated(*args, **kwargs):
            client_id = request.remote_addr
            
            if not self.is_allowed(client_id):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'retry_after': self.window
                }), 429
                
            return f(*args, **kwargs)
        return decorated
