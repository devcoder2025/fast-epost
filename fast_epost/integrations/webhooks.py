from dataclasses import dataclass
from typing import Dict, Any, List
import requests
import json

@dataclass
class WebhookEvent:
    event_type: str
    payload: Dict[str, Any]
    timestamp: str

class WebhookManager:
    def __init__(self):
        self.webhooks: Dict[str, List[str]] = {}
        
    def register(self, event_type: str, endpoint: str):
        if event_type not in self.webhooks:
            self.webhooks[event_type] = []
        self.webhooks[event_type].append(endpoint)
        
    def trigger(self, event: WebhookEvent):
        endpoints = self.webhooks.get(event.event_type, [])
        for endpoint in endpoints:
            requests.post(endpoint, json=event.__dict__)
