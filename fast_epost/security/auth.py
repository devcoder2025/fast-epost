
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
from functools import wraps
from flask import request, jsonify

class JWTAuth:
    def __init__(self, secret_key: str, token_expiry: int = 3600):
        self.secret_key = secret_key
        self.token_expiry = token_expiry

    def generate_token(self, user_data: Dict) -> str:
        payload = {
            **user_data,
            'exp': datetime.utcnow() + timedelta(seconds=self.token_expiry),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def verify_token(self, token: str) -> Optional[Dict]:
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return None

    def token_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing'}), 401
            
            payload = self.verify_token(token.split(' ')[1])
            if not payload:
                return jsonify({'message': 'Invalid token'}), 401
                
            return f(*args, **kwargs)
        return decorated
