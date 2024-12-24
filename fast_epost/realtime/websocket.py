import asyncio
from typing import Dict, Set
from dataclasses import dataclass

@dataclass
class Client:
    id: str
    channel: str
    websocket: object

class WebSocketManager:
    def __init__(self):
        self.clients = set()
        self.channels = {}
        
    async def connect(self, client):
        self.clients.add(client)
        if client.channel not in self.channels:
            self.channels[client.channel] = set()
        self.channels[client.channel].add(client)
        
    async def broadcast(self, channel, message):
        if channel in self.channels:
            tasks = [client.send_json(message) for client in self.channels[channel]]
            await asyncio.gather(*tasks)