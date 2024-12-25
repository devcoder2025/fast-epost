
from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Optional, Dict, Any
from .auth import AuthManager, User
import asyncio
from src.analytics.dashboard import AnalyticsDashboard
from src.collector.link_collector import AsyncLinkCollector
from src.build.pyproject import EnhancedPyProjectManager

class APIGateway:
    def __init__(self, secret_key: str):
        self.app = FastAPI()
        self.auth = AuthManager(secret_key)
        self.analytics = AnalyticsDashboard()
        self.collector = AsyncLinkCollector()
        self.build_manager = EnhancedPyProjectManager(".")
        
        self._setup_routes()

    def _setup_routes(self):
        @self.app.post("/api/register")
        async def register_user(username: str):
            user = self.auth.register_user(username)
            return {"api_key": user.api_key}

        @self.app.post("/api/token")
        async def create_token(username: str):
            token = self.auth.create_token(username)
            return {"token": token}

        @self.app.get("/api/metrics")
        async def get_metrics(user: User = Depends(self._get_current_user)):
            return self.analytics.metrics.get_metrics_snapshot()

        @self.app.post("/api/collect")
        async def collect_links(
            urls: list,
            user: User = Depends(self._get_current_user)
        ):
            results = await self.collector.collect_links(urls)
            return {"links": results}

        @self.app.post("/api/build")
        async def build_project(
            config: Dict[str, Any],
            user: User = Depends(self._get_current_user)
        ):
            await self.build_manager.build_project()
            return {"status": "success"}

    async def _get_current_user(
        self,
        authorization: Optional[str] = Header(None),
        x_api_key: Optional[str] = Header(None)
    ) -> User:
        if authorization:
            token = authorization.split()[-1]
            user = self.auth.validate_token(token)
            if user:
                return user

        if x_api_key:
            user = self.auth.validate_api_key(x_api_key)
            if user:
                return user

        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )

    async def start(self, host: str = "0.0.0.0", port: int = 8000):
        analytics_task = asyncio.create_task(
            self.analytics.start(host=host, port=port+1)
        )
        await self.app.start(host=host, port=port)
        await analytics_task
