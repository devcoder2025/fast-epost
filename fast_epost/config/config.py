class ConfigManager:
    def __init__(self):
        self.providers = []

    def add_provider(self, provider):
        self.providers.append(provider)

    async def get(self, key):
        for provider in self.providers:
            value = await provider.get(key)
            if value is not None:
                return value
        return None

class FileConfigProvider:
    def __init__(self, file_path):
        self.file_path = file_path

    async def get(self, key):
        try:
            async with aiofiles.open(self.file_path, mode='r') as f:
                config = json.load(f)
                return config.get(key)
        except Exception as e:
            logging.error(f"Error reading config from {self.file_path}: {e}")
            return None
class FileConfigProvider:
    def __init__(self, file_path):
        self.file_path = file_path

    async def get(self, key):
        try:
            async with aiofiles.open(self.file_path, mode='r') as f:
                config = json.load(f)
                return config.get(key)
        except Exception as e:
            logging.error(f"Error reading config from {self.file_path}: {e}")
            return None


class ConsulConfigProvider:
    async def get(self, key):
        # Placeholder for getting a value from Consul
        return None
