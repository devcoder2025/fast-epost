
from typing import Dict, Any, Optional
import asyncio
import yaml
import json
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .store import ConfigStore

class ConfigManager:
    def __init__(self, config_dir: str):
        self.config_dir = Path(config_dir)
        self.store = ConfigStore()
        self.observer = Observer()
        self._setup_watchers()

    def _setup_watchers(self):
        event_handler = ConfigFileHandler(self)
        self.observer.schedule(
            event_handler,
            str(self.config_dir),
            recursive=False
        )

    def start(self):
        self._load_all_configs()
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

    def _load_all_configs(self):
        for config_file in self.config_dir.glob("*.{yaml,yml,json}"):
            self._load_config_file(config_file)

    def _load_config_file(self, file_path: Path):
        try:
            with open(file_path, 'r') as f:
                if file_path.suffix in ('.yaml', '.yml'):
                    config = yaml.safe_load(f)
                else:
                    config = json.load(f)
                
                namespace = file_path.stem
                self.store.set_namespace(namespace, config)
                
        except Exception as e:
            print(f"Error loading config file {file_path}: {e}")

    def get_config(self, namespace: str, key: str) -> Any:
        return self.store.get(namespace, key)

    def set_config(self, namespace: str, key: str, value: Any):
        self.store.set(namespace, key, value)
        self._save_config(namespace)

    def _save_config(self, namespace: str):
        config = self.store.get_namespace(namespace)
        if not config:
            return

        file_path = self.config_dir / f"{namespace}.yaml"
        with open(file_path, 'w') as f:
            yaml.safe_dump(config, f)

class ConfigFileHandler(FileSystemEventHandler):
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager

    def on_modified(self, event):
        if not event.is_directory:
            file_path = Path(event.src_path)
            if file_path.suffix in ('.yaml', '.yml', '.json'):
                self.config_manager._load_config_file(file_path)
