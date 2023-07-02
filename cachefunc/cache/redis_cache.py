from pickle import loads, dumps
from redis import Redis
from typing import Any

from cachefunc.cache.base import BaseCache, NotCached


class RedisCache(BaseCache):
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.redis = Redis(host, port, db)

    def _get(self, key: int) -> Any:
        if (result := self.redis.get(key)) is not None:
            return loads(result)
        raise NotCached()

    def _set(self, key: int, result: Any, **kwargs) -> None:
        self.redis.set(key, dumps(result))