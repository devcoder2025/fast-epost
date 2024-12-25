
import pytest
from unittest.mock import Mock, patch
import asyncio
from src.discovery.registry import ServiceRegistry, ServiceInstance
from src.discovery.client import ServiceDiscoveryClient

@pytest.fixture
def registry():
    return ServiceRegistry(heartbeat_timeout=5)

@pytest.fixture
def client(registry):
    return ServiceDiscoveryClient(registry)

@pytest.mark.asyncio
async def test_service_registration(registry):
    instance_id = await registry.register_service(
        "test-service",
        "localhost",
        8080
    )
    assert "test-service" in registry.services
    assert instance_id in registry.services["test-service"]

@pytest.mark.asyncio
async def test_service_heartbeat(registry):
    instance_id = await registry.register_service(
        "test-service",
        "localhost",
        8080
    )
    assert await registry.heartbeat("test-service", instance_id)

@pytest.mark.asyncio
async def test_service_discovery(client):
    await client.registry.register_service(
        "test-service",
        "localhost",
        8080
    )
    
    instance = await client.get_service_instance("test-service")
    assert instance is not None
    assert instance.host == "localhost"
    assert instance.port == 8080

@pytest.mark.asyncio
async def test_service_health_check(registry):
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = Mock()
        mock_response.status = 200
        mock_get.return_value.__aenter__.return_value = mock_response
        
        instance_id = await registry.register_service(
            "test-service",
            "localhost",
            8080
        )
        await registry._check_services_health()
        
        instance = registry.services["test-service"][instance_id]
        assert instance.status == "UP"

@pytest.mark.asyncio
async def test_service_call(client):
    await client.registry.register_service(
        "test-service",
        "localhost",
        8080
    )
    
    with patch('aiohttp.ClientSession.request') as mock_request:
        mock_response = Mock()
        mock_response.json = asyncio.coroutine(lambda: {"status": "ok"})
        mock_request.return_value.__aenter__.return_value = mock_response
        
        result = await client.call_service("test-service", "/test")
        assert result["status"] == "ok"
