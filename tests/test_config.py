import pytest
import asyncio
import tempfile
import json
import yaml
from pathlib import Path
from src.config.manager import ConfigManager
from src.config.providers import FileConfigProvider, ConsulConfigProvider

@pytest.fixture
def config_manager():
    return ConfigManager()

@pytest.fixture
def temp_config_file():
    with tempfile.NamedTemporaryFile(suffix='.yaml') as tmp:
        yield tmp.name

@pytest.mark.asyncio
async def test_file_config_provider(temp_config_file):
    initial_config = {
        'database': {
            'host': 'localhost',
            'port': 5432
        }
    }
    
    with open(temp_config_file, 'w') as f:
        yaml.dump(initial_config, f)
    
    provider = FileConfigProvider(temp_config_file)
    manager = ConfigManager()
    manager.add_provider(provider)
    
    value = await manager.get('database.host')
    assert value == 'localhost'

@pytest.mark.asyncio
async def test_config_watchers(config_manager, temp_config_file):
    provider = FileConfigProvider(temp_config_file)
    config_manager.add_provider(provider)
    
    changes = []
    async def watcher(key, new_value, old_value):
        changes.append((key, new_value, old_value))
    
    config_manager.watch('test.key', watcher)
    await config_manager.set('test.key', 'value1')
    await config_manager.set('test.key', 'value2')
    
    assert len(changes) == 2
    assert changes[0] == ('test.key', 'value1', None)
    assert changes[1] == ('test.key', 'value2', 'value1')

@pytest.mark.asyncio
async def test_multiple_providers(config_manager):
    file_provider = FileConfigProvider('config1.yaml')
    consul_provider = ConsulConfigProvider()
    
    config_manager.add_provider(file_provider)
    config_manager.add_provider(consul_provider)
    
    # Provider order should be respected
    providers = config_manager.providers
    assert len(providers) == 2
    assert isinstance(providers[0], FileConfigProvider)
    assert isinstance(providers[1], ConsulConfigProvider)

@pytest.mark.asyncio
async def test_config_refresh(config_manager, temp_config_file):
    provider = FileConfigProvider(temp_config_file)
    config_manager.add_provider(provider)
    config_manager.refresh_interval = 0.1
    
    await config_manager.set('test.key', 'initial')
    initial_value = await config_manager.get('test.key')
    assert initial_value == 'initial'
    
    # Simulate external config change
    with open(temp_config_file, 'w') as f:
        yaml.dump({'test': {'key': 'updated'}}, f)
    
    await config_manager.start()
    await asyncio.sleep(0.2)
    
    updated_value = await config_manager.get('test.key')
    assert updated_value == 'updated'
    
    await config_manager.stop()
