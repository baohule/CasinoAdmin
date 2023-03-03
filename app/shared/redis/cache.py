from fastapi.logger import logger
from fastapi_cache import caches
from app.shared.middleware.json_encoders import decode_model
from app.shared.utils.timer import Timer


class RedisCache:
    def __init__(self):
        self.cache = caches.get("CACHE_KEY")

    async def check_cache(self, key):
        in_cache = await self.cache.get(key)
        if in_cache:
            try:
                model = decode_model(in_cache)
            except TypeError as e:
                logger.info(e)
                model = None
            return model
        return None

    async def put_in_cache(self, key, value, expire_time=None):
        in_cache = await self.check_cache(key)
        if not in_cache:
            await self.cache.set(key, value)
            if expire_time:
                await self.cache.expire(key=key, ttl=expire_time)

    async def get_posts_from_cache(self, cache_key):
        cache_data: list = await self.check_cache(cache_key)
        if cache_data:
            logger.info(f"fetching {cache_key} from cache")
            return cache_data

    async def get_trending_from_cache(self, content_filter):
        cache_data: list = await self.check_cache(f"trending_{content_filter}")
        if cache_data:
            logger.info(f"fetching {content_filter} from cache")
            return cache_data

    async def cache_singe_post(self, post: dict, post_id: str):
        cache_key = f"{post_id}"
        await self.put_in_cache(cache_key, post)
        logger.info(f"stored {post_id} in cache")
