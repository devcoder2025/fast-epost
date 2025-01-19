from dataclasses import dataclass
from typing import List, Dict
import yaml

@dataclass
class APIEndpoint:
    path: str
    method: str
    description: str
    parameters: Dict
    responses: Dict

class APIDocGenerator:
    def __init__(self):
        self.endpoints: List[APIEndpoint] = []
        
    def document_endpoint(self, endpoint: APIEndpoint):
        self.endpoints.append(endpoint)
        
    def generate_yaml(self) -> str:
        return yaml.dump({'endpoints': self.endpoints})
