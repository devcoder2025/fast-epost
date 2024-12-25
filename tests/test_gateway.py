
import pytest
from fastapi.testclient import TestClient
from src.gateway.api import APIGateway
from src.gateway.auth import AuthManager, User

@pytest.fixture
def auth_manager():
    return AuthManager("test_secret")

@pytest.fixture
def api_gateway():
    return APIGateway("test_secret")

@pytest.fixture
def client(api_gateway):
    return TestClient(api_gateway.app)

def test_user_registration(auth_manager):
    user = auth_manager.register_user("testuser")
    assert isinstance(user, User)
    assert user.username == "testuser"
    assert user.api_key is not None

def test_token_creation(auth_manager):
    user = auth_manager.register_user("testuser")
    token = auth_manager.create_token("testuser")
    assert auth_manager.validate_token(token) == user

def test_api_key_validation(auth_manager):
    user = auth_manager.register_user("testuser")
    assert auth_manager.validate_api_key(user.api_key) == user
    assert auth_manager.validate_api_key("invalid_key") is None

def test_api_endpoints(client):
    # Register user
    response = client.post("/api/register?username=testuser")
    assert response.status_code == 200
    api_key = response.json()["api_key"]

    # Test with API key
    headers = {"X-API-Key": api_key}
    response = client.get("/api/metrics", headers=headers)
    assert response.status_code == 200

    # Test without authentication
    response = client.get("/api/metrics")
    assert response.status_code == 401

def test_token_revocation(auth_manager):
    user = auth_manager.register_user("testuser")
    token = auth_manager.create_token("testuser")
    auth_manager.revoke_token(token)
    assert auth_manager.validate_token(token) is None
