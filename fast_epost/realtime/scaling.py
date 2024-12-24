import redis

class RedisScaling:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.pubsub = self.redis.pubsub()
        
    async def publish(self, channel: str, message: dict):
        self.redis.publish(channel, json.dumps(message))
        
    async def subscribe(self, channel: str):
        self.pubsub.subscribe(channel)
