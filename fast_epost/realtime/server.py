from fastapi import FastAPI, WebSocket
from .websocket import WebSocketManager
from .messages import MessageHandler
from .channels import ChannelManager
from .presence import PresenceTracker

class RealtimeServer:
    def __init__(self):
        self.app = FastAPI()
        self.ws_manager = WebSocketManager()
        self.message_handler = MessageHandler(self.ws_manager)
        self.channel_manager = ChannelManager()
        self.presence = PresenceTracker()
        
    async def handle_connection(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        client = Client(id=client_id, channel='main', websocket=websocket)
        await self.ws_manager.connect(client)
        self.presence.mark_online(client_id)
        
        try:
            while True:
                data = await websocket.receive_json()
                await self.message_handler.process_message(Message(**data))
        finally:
            self.presence.mark_offline(client_id)
