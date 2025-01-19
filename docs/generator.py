from dataclasses import dataclass
from typing import Dict, List
import yaml

@dataclass
class APIEndpoint:
    path: str
    method: str
    description: str
    parameters: Dict
    responses: Dict

class SwaggerGenerator:
    def __init__(self, title: str, version: str):
        self.title = title
        self.version = version
        self.endpoints: List[APIEndpoint] = []
        
    def add_endpoint(self, endpoint: APIEndpoint):
        self.endpoints.append(endpoint)
        
    def generate_spec(self) -> Dict:
        return {
            'openapi': '3.0.0',
            'info': {
                'title': self.title,
                'version': self.version
            },
            'paths': self._generate_paths()
        }
