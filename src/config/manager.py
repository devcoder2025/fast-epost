from typing import Any, Dict, Optional, List
import asyncio
import json
import yaml
from pathlib import Path
from dataclasses import dataclass
import logging

@dataclass
class ConfigValue:
    key: str
    value: Any
    source: str
    version: Optional[int] = None
    last_updated: Optional[float] = None

class ConfigManager:
    def __init__(self):
        self.providers = []
        self.watchers = {}
        self.cache: Dict[str, ConfigValue] = {}
        self.logger = logging.getLogger(__name__)
        self._running = False
        self.refresh_interval = 30

    def add_provider(self, provider):
        self.providers.append(provider)

    def watch(self, key: str, callback):
        if key not in self.watchers:
            self.watchers[key] = set()
        self.watchers[key].add(callback)

    def unwatch(self, key: str, callback):
        if key in self.watchers:
            self.watchers[key].discard(callback)
            if not self.watchers[key]:
                del self.watchers[key]

    async def get(self, key: str, default: Any = None) -> Any:
        if key in self.cache:
            return self.cache[key].value

        for provider in reversed(self.providers):
            try:
                value = await provider.get(key)
                if value is not None:
                    self.cache[key] = ConfigValue(
                        key=key,
                        value=value,
                        source=provider.name
                    )
                    return value
            except Exception as e:
                self.logger.error(f"Error getting config from {provider.name}: {e}")

        return default

    async def set(self, key: str, value: Any):
        if not self.providers:
            raise ValueError("No config providers available")

        provider = self.providers[-1]
        await provider.set(key, value)
        
        old_value = self.cache.get(key)
        self.cache[key] = ConfigValue(
            key=key,
            value=value,
            source=provider.name
        )

        if key in self.watchers:
            await self._notify_watchers(key, value, old_value)

    async def _notify_watchers(self, key: str, new_value: Any, old_value: Optional[ConfigValue]):
        if key in self.watchers:
            for callback in self.watchers[key]:
                try:
                    await callback(key, new_value, old_value.value if old_value else None)
                except Exception as e:
                    self.logger.error(f"Error notifying config watcher: {e}")

    async def start(self):
        self._running = True
        asyncio.create_task(self._refresh_loop())

    async def stop(self):
        self._running = False

    async def _refresh_loop(self):
        while self._running:
            await self._refresh_configs()
            await asyncio.sleep(self.refresh_interval)

    async def _refresh_configs(self):
        for key in list(self.cache.keys()):
            old_value = self.cache[key]
            new_value = await self.get(key)
            
            if new_value != old_value.value:
                await self._notify_watchers(key, new_value, old_value)