from typing import Dict, Set
import asyncio

class ChannelManager:
    def __init__(self):
        self.channels: Dict[str, Set[str]] = {}
        self.user_channels: Dict[str, Set[str]] = {}
        
    async def create_channel(self, channel_id: str, owner: str):
        self.channels[channel_id] = {owner}
        if owner not in self.user_channels:
            self.user_channels[owner] = set()
        self.user_channels[owner].add(channel_id)
        
    async def join_channel(self, channel_id: str, user_id: str):
        if channel_id in self.channels:
            self.channels[channel_id].add(user_id)
            if user_id not in self.user_channels:
                self.user_channels[user_id] = set()
            self.user_channels[user_id].add(channel_id)
