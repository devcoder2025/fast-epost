
import logging
from datetime import datetime
from typing import Any, Dict
import json
from pathlib import Path

class AuditLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup file handler
        self.logger = logging.getLogger('audit')
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(self.log_dir / 'audit.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_event(self, event_type: str, user_id: str, data: Dict[str, Any]) -> None:
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'data': data
        }
        self.logger.info(json.dumps(log_entry))

    def get_user_activity(self, user_id: str) -> list:
        activities = []
        with open(self.log_dir / 'audit.log', 'r') as f:
            for line in f:
                if user_id in line:
                    activities.append(json.loads(line.split(' - ')[-1]))
        return activities
