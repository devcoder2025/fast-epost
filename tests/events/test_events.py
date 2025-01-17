
import pytest
import asyncio
from src.events.bus import EventBus, Event
from src.events.handlers import EventHandler, RetryHandler

@pytest.fixture
def event_bus():
    return EventBus()

@pytest.mark.asyncio
async def test_event_publishing(event_bus):
    received_events = []
    
    async def handler(event):
        received_events.append(event)
    
    event_bus.subscribe("test_event", handler)
    event = Event("test_event", {"data": "test"})
    
    await event_bus.publish(event)
    await event_bus.start()
    await asyncio.sleep(0.1)
    
    assert len(received_events) == 1
    assert received_events[0].data["data"] == "test"

@pytest.mark.asyncio
async def test_multiple_handlers(event_bus):
    results = []
    
    async def handler1(event):
        results.append(1)
    
    async def handler2(event):
        results.append(2)
    
    event_bus.subscribe("test_event", handler1)
    event_bus.subscribe("test_event", handler2)
    
    event = Event("test_event", {})
    await event_bus.publish(event)
    await event_bus.start()
    await asyncio.sleep(0.1)
    
    assert sorted(results) == [1, 2]

@pytest.mark.asyncio
async def test_middleware(event_bus):
    async def middleware(event):
        event.data["modified"] = True
        return event
    
    received_event = None
    async def handler(event):
        nonlocal received_event
        received_event = event
    
    event_bus.add_middleware(middleware)
    event_bus.subscribe("test_event", handler)
    
    event = Event("test_event", {})
    await event_bus.publish(event)
    await event_bus.start()
    await asyncio.sleep(0.1)
    
    assert received_event.data["modified"] is True

@pytest.mark.asyncio
async def test_retry_handler():
    fail_count = 0
    
    async def failing_handler(event):
        nonlocal fail_count
        fail_count += 1
        if fail_count < 3:
            raise ValueError("Simulated failure")
        return "success"
    
    handler = RetryHandler(failing_handler, max_retries=3, retry_delay=0.1)
    result = await handler(Event("test_event", {}))
    
    assert result == "success"
    assert fail_count == 3
