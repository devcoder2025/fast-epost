import pytest
import asyncio
from src.discovery.registry import ServiceRegistry, ServiceInstance
from src.discovery.providers import ConsulServiceProvider

@pytest.fixture
def registry():
    return ServiceRegistry(heartbeat_interval=1, cleanup_interval=2)

@pytest.mark.asyncio
async def test_service_registration(registry):
    instance = await registry.register(
        "test-service",
        "localhost",
        8080,
        {"version": "1.0"}
    )
    
    assert instance.name == "test-service"
    assert instance.host == "localhost"
    assert instance.port == 8080
    assert instance.metadata == {"version": "1.0"}
    
    instances = registry.get_instances("test-service")
    assert len(instances) == 1
    assert instances[0].id == instance.id

@pytest.mark.asyncio
async def test_service_heartbeat(registry):
    instance = await registry.register("test-service", "localhost", 8080)
    instance_id = instance.id
    
    # Verify heartbeat updates last_heartbeat
    initial_heartbeat = instance.last_heartbeat
    await asyncio.sleep(0.1)
    await registry.heartbeat("test-service", instance_id)
    
    updated_instance = registry.get_instances("test-service")[0]
    assert updated_instance.last_heartbeat > initial_heartbeat

@pytest.mark.asyncio
async def test_service_cleanup(registry):
    instance = await registry.register("test-service", "localhost", 8080)
    
    # Wait for cleanup
    await registry.start()
    await asyncio.sleep(3)
    
    # Service should be marked as down
    instances = registry.get_instances("test-service")
    assert instances[0].status == "down"
    
    await registry.stop()

@pytest.mark.asyncio
async def test_service_watchers(registry):
    events = []
    
    async def watcher(event, instance):
        events.append((event, instance.id))
    
    registry.watch("test-service", watcher)
    
    instance = await registry.register("test-service", "localhost", 8080)
    await registry.deregister("test-service", instance.id)
    
    assert len(events) == 2
    assert events[0][0] == "register"
    assert events[1][0] == "deregister"

@pytest.mark.asyncio
async def test_multiple_instances(registry):
    await registry.register("test-service", "host1", 8080)
    await registry.register("test-service", "host2", 8080)
    
    instances = registry.get_instances("test-service")
    assert len(instances) == 2
    assert {i.host for i in instances} == {"host1", "host2"}
