
from typing import Optional, Dict
import jwt
from datetime import datetime, timedelta
from dataclasses import dataclass
import hashlib
import secrets

@dataclass
class User:
    username: str
    role: str
    api_key: str

class AuthManager:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.users: Dict[str, User] = {}
        self.token_blacklist: set = set()

    def register_user(self, username: str, role: str = "user") -> User:
        api_key = self._generate_api_key()
        user = User(username=username, role=role, api_key=api_key)
        self.users[username] = user
        return user

    def create_token(self, username: str) -> str:
        if username not in self.users:
            raise ValueError("User not found")

        payload = {
            'username': username,
            'role': self.users[username].role,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def validate_token(self, token: str) -> Optional[User]:
        if token in self.token_blacklist:
            return None

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            username = payload['username']
            return self.users.get(username)
        except jwt.InvalidTokenError:
            return None

    def validate_api_key(self, api_key: str) -> Optional[User]:
        for user in self.users.values():
            if user.api_key == api_key:
                return user
        return None

    def revoke_token(self, token: str) -> None:
        self.token_blacklist.add(token)

    def _generate_api_key(self) -> str:
        random_bytes = secrets.token_bytes(32)
        return hashlib.sha256(random_bytes).hexdigest()
