from dataclasses import dataclass
from typing import Any, Dict
import json

@dataclass
class Message:
    channel: str
    event: str
    data: Dict[str, Any]
    sender: str

class MessageHandler:
    def __init__(self, ws_manager):
        self.ws_manager = ws_manager
        self.handlers = {}
        
    def register_handler(self, event, handler):
        self.handlers[event] = handler
        
    async def process_message(self, message):
        if handler := self.handlers.get(message.event):
            response = await handler(message.data)
            await self.ws_manager.broadcast(message.channel, response)
