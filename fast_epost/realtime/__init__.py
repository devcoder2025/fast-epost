from .websocket import WebSocketManager
from .messages import MessageHandler
from .channels import ChannelManager
from .presence import PresenceTracker
from .events import EventEmitter
from .scaling import RedisScaling

class RealtimeSystem:
    def __init__(self, redis_url: str = None):
        self.ws_manager = WebSocketManager()
        self.message_handler = MessageHandler(self.ws_manager)
        self.channel_manager = ChannelManager()
        self.presence = PresenceTracker()
        self.events = EventEmitter()
        self.scaling = RedisScaling(redis_url) if redis_url else None
