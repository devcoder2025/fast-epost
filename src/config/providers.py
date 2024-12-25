
from typing import Any, Dict, Optional
import json
import yaml
import aiofiles
import aiohttp
from abc import ABC, abstractmethod
from pathlib import Path

class ConfigProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any):
        pass

class FileConfigProvider(ConfigProvider):
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self._config = {}
        self._load_config()

    @property
    def name(self) -> str:
        return f"file:{self.filepath}"

    def _load_config(self):
        if not self.filepath.exists():
            return

        content = self.filepath.read_text()
        if self.filepath.suffix in ('.yaml', '.yml'):
            self._config = yaml.safe_load(content)
        elif self.filepath.suffix == '.json':
            self._config = json.loads(content)
        else:
            raise ValueError(f"Unsupported file format: {self.filepath.suffix}")

    async def get(self, key: str) -> Optional[Any]:
        keys = key.split('.')
        value = self._config
        for k in keys:
            if not isinstance(value, dict):
                return None
            value = value.get(k)
        return value

    async def set(self, key: str, value: Any):
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value

        content = (
            yaml.dump(self._config)
            if self.filepath.suffix in ('.yaml', '.yml')
            else json.dumps(self._config, indent=2)
        )
        
        async with aiofiles.open(self.filepath, 'w') as f:
            await f.write(content)

class ConsulConfigProvider(ConfigProvider):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8500,
        prefix: str = "config/"
    ):
        self.base_url = f"http://{host}:{port}/v1/kv/"
        self.prefix = prefix

    @property
    def name(self) -> str:
        return "consul"

    async def get(self, key: str) -> Optional[Any]:
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}{self.prefix}{key}"
            async with session.get(url) as response:
                if response.status == 404:
                    return None
                if response.status != 200:
                    raise Exception(f"Failed to get config from Consul: {response.status}")
                
                data = await response.json()
                if not data:
                    return None
                
                try:
                    return json.loads(data[0]["Value"])
                except (json.JSONDecodeError, KeyError):
                    return None

    async def set(self, key: str, value: Any):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}{self.prefix}{key}"
            async with session.put(url, json=value) as response:
                if response.status != 200:
                    raise Exception(f"Failed to set config in Consul: {response.status}")
