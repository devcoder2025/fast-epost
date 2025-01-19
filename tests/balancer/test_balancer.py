
import pytest
from unittest.mock import Mock, patch
import asyncio
from src.balancer.load_balancer import LoadBalancer, NoHealthyServersError
from src.balancer.health_check import HealthChecker

@pytest.fixture
def servers():
    return [
        "http://server1:8000",
        "http://server2:8000",
        "http://server3:8000"
    ]

@pytest.fixture
def load_balancer(servers):
    return LoadBalancer(servers)

@pytest.mark.asyncio
async def test_health_checker():
    checker = HealthChecker(check_interval=1)
    await checker.add_server("http://test:8000")
    
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value = Mock(status=200)
        await checker._check_server("http://test:8000")
        
        server_health = checker.servers["http://test:8000"]
        assert server_health.healthy
        assert server_health.error_count == 0

@pytest.mark.asyncio
async def test_load_balancer_request(load_balancer):
    with patch('aiohttp.ClientSession.request') as mock_request:
        mock_response = Mock()
        mock_response.json = asyncio.coroutine(lambda: {"status": "ok"})
        mock_request.return_value.__aenter__.return_value = mock_response
        
        response = await load_balancer.handle_request("/test")
        assert response["status"] == "ok"

@pytest.mark.asyncio
async def test_server_selection(load_balancer):
    # Mark all servers as healthy
    for server in load_balancer.stats:
        await load_balancer.health_checker.add_server(server)
        health = load_balancer.health_checker.servers[server]
        health.healthy = True
    
    selected_server = load_balancer._select_server()
    assert selected_server in load_balancer.stats

@pytest.mark.asyncio
async def test_no_healthy_servers(load_balancer):
    # Mark all servers as unhealthy
    for server in load_balancer.stats:
        await load_balancer.health_checker.add_server(server)
        health = load_balancer.health_checker.servers[server]
        health.healthy = False
    
    with pytest.raises(NoHealthyServersError):
        await load_balancer.handle_request("/test")

def test_stats_tracking(load_balancer):
    server = list(load_balancer.stats.keys())[0]
    stats = load_balancer.stats[server]
    
    load_balancer._update_stats(server, True, 0.1)
    assert stats.requests == 1
    assert stats.errors == 0
    assert stats.total_response_time == 0.1
