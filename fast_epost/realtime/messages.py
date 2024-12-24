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
    def __init__(self, websocket_manager):
        self.ws_manager = websocket_manager
        self.handlers = {}
        
    def register_handler(self, event: str, handler: callable):
        self.handlers[event] = handler
        
    async def process_message(self, message: Message):
        if handler := self.handlers.get(message.event):
            response = await handler(message.data)
            await self.ws_manager.broadcast(
                message.channel,
                {
                    'event': message.event,
                    'data': response,
                    'sender': message.sender
                }
            )
