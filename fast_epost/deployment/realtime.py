import socketio
from typing import Dict

class DeploymentSocket:
    def __init__(self):
        self.sio = socketio.AsyncServer(async_mode='asgi')
        self.connected_clients = set()
        
    async def broadcast_status(self, data: Dict):
        await self.sio.emit('deployment_update', data)
        
    def register_handlers(self):
        @self.sio.on('connect')
        async def connect(sid, environ):
            self.connected_clients.add(sid)
            
        @self.sio.on('disconnect')
        async def disconnect(sid):
            self.connected_clients.remove(sid)
