from datetime import datetime

class PresenceTracker:
    def __init__(self):
        self.online_users = {}
        
    def mark_online(self, user_id: str):
        self.online_users[user_id] = datetime.now()
        
    def mark_offline(self, user_id: str):
        if user_id in self.online_users:
            del self.online_users[user_id]
            
    def get_online_users(self):
        return list(self.online_users.keys())
