from typing import Optional
import redis

class SearchCache:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.ttl = 3600  # 1 hour
        
    async def get_cached_results(self, query_hash: str) -> Optional[Dict]:
        cached = await self.redis.get(query_hash)
        return json.loads(cached) if cached else None
        
    async def cache_results(self, query_hash: str, results: Dict):
        await self.redis.setex(
            query_hash,
            self.ttl,
            json.dumps(results)
        )
