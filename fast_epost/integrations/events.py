from typing import Callable, Dict, List
import asyncio

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        
    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        
    async def publish(self, event_type: str, data: Dict):
        callbacks = self.subscribers.get(event_type, [])
        tasks = [callback(data) for callback in callbacks]
        await asyncio.gather(*tasks)
