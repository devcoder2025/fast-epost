from abc import ABC, abstractmethod
from typing import BinaryIO, Optional

class StorageBackend(ABC):
    @abstractmethod
    def save(self, file_path: str, content: BinaryIO) -> str:
        pass
        
    @abstractmethod
    def get(self, file_path: str) -> Optional[BinaryIO]:
        pass
