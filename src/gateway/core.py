from typing import Dict, List, Optional, Callable
import asyncio
import aiohttp
from datetime import datetime
import jwt
from fastapi import FastAPI, Request, Response, HTTPException
from .rate_limiter import RateLimiter
from .cache import CacheManager

class APIGateway:
    def __init__(self):
        self.app = FastAPI()
        self.routes: Dict[str, str] = {}
        self.rate_limiter = RateLimiter()
        self.cache = CacheManager()
        self.middlewares: List[Callable] = []
        self._setup_middleware()

    def _setup_middleware(self):
        @self.app.middleware("http")
        async def gateway_middleware(request: Request, call_next):
            # Rate limiting check
            if not await self.rate_limiter.allow_request(request):
                raise HTTPException(status_code=429, detail="Too many requests")

            # Route handling
            path = request.url.path
            if path in self.routes:
                return await self._handle_proxy(request, self.routes[path])
            
            return await call_next(request)

    async def _handle_proxy(self, request: Request, target_url: str):
        async with aiohttp.ClientSession() as session:
            # Cache check
            cache_key = f"{request.method}:{request.url}"
            cached_response = await self.cache.get(cache_key)
            if cached_response:
                return Response(**cached_response)

            # Forward request
            async with session.request(
                method=request.method,
                url=f"{target_url}{request.url.path}",
                headers=dict(request.headers),
                data=await request.body()
            ) as response:
                content = await response.read()
                return Response(
                    content=content,
                    status_code=response.status,
                    headers=dict(response.headers)
                )
