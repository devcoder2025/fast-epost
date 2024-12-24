class EventEmitter:
    def __init__(self):
        self.listeners = {}
        
    async def emit(self, event, data):
        if event in self.listeners:
            for callback in self.listeners[event]:
                await callback(data)
