class EventEmitter:
    def __init__(self):
        self.listeners = {}
        
    def on(self, event: str, callback: callable):
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)
        
    async def emit(self, event: str, data: dict):
        if event in self.listeners:
            for callback in self.listeners[event]:
                await callback(data)
