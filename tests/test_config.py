
import pytest
import tempfile
from pathlib import Path
import yaml
import time
from src.config.manager import ConfigManager
from src.config.store import ConfigStore

@pytest.fixture
def config_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def config_manager(config_dir):
    manager = ConfigManager(config_dir)
    manager.start()
    yield manager
    manager.stop()

@pytest.fixture
def config_store():
    return ConfigStore()

def test_config_loading(config_dir, config_manager):
    config_path = Path(config_dir) / "test.yaml"
    config_data = {
        "database": {
            "host": "localhost",
            "port": 5432
        }
    }
    
    with open(config_path, 'w') as f:
        yaml.safe_dump(config_data, f)
    
    time.sleep(1)  # Wait for file watcher
    assert config_manager.get_config("test", "database.host") == "localhost"
    assert config_manager.get_config("test", "database.port") == 5432

def test_config_store():
    store = ConfigStore()
    store.set_namespace("app", {
        "server": {
            "host": "localhost",
            "port": 8080
        }
    })
    
    assert store.get("app", "server.host") == "localhost"
    assert store.get("app", "server.port") == 8080

def test_config_update(config_dir, config_manager):
    config_manager.set_config("app", "server.port", 9000)
    assert config_manager.get_config("app", "server.port") == 9000
    
    config_path = Path(config_dir) / "app.yaml"
    assert config_path.exists()
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        assert config["server"]["port"] == 9000

def test_nested_config(config_store):
    config_store.set("app", "database.credentials.username", "admin")
    assert config_store.get("app", "database.credentials.username") == "admin"

def test_config_deletion(config_store):
    config_store.set_namespace("test", {"key": "value"})
    config_store.delete_namespace("test")
    assert config_store.get_namespace("test") is None
