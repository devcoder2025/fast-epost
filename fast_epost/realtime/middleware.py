class RealtimeMiddleware:
    def __init__(self, app):
        self.app = app
        
    async def __call__(self, scope, receive, send):
        if scope['type'] == 'websocket':
            await self.handle_websocket(scope, receive, send)
        await self.app(scope, receive, send)
        
    async def handle_websocket(self, scope, receive, send):
        client_id = scope['client'][0]
        await self.app.realtime.handle_connection(scope, receive, send, client_id)
