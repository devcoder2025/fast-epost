import pytest
from typing import Generator, Any
from contextlib import contextmanager

class TestClient:
    def __init__(self, app):
        self.app = app
        self.client = app.test_client()
        
    def get(self, *args, **kwargs):
        return self.client.get(*args, **kwargs)
        
    def post(self, *args, **kwargs):
        return self.client.post(*args, **kwargs)

@pytest.fixture
def test_app() -> Generator[Any, Any, Any]:
    from fast_epost.app import app
    with app.test_client() as client:
        yield client

class MockStorage:
    def __init__(self):
        self.stored_files = {}
        
    def store_file(self, path: str, content: bytes):
        self.stored_files[path] = content
        
    def get_file(self, path: str):
        return self.stored_files.get(path)

@contextmanager
def mock_storage():
    storage = MockStorage()
    yield storage
