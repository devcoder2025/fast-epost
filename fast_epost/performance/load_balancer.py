from typing import List, Dict
import random

class LoadBalancer:
    def __init__(self):
        self.servers: List[str] = []
        self.health_checks: Dict[str, bool] = {}
        
    def add_server(self, server_url: str):
        self.servers.append(server_url)
        self.health_checks[server_url] = True
        
    def get_next_server(self) -> str:
        available = [s for s in self.servers if self.health_checks[s]]
        return random.choice(available)
