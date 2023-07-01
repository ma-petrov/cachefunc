from pickle import loads, dumps
from redis import Redis
from typing import Any, Hashable

from cachefunc.cache.base import BaseCache, NotCached


class RedisCache(BaseCache):
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.redis = Redis(host, port, db)

    def _get(self, key: Hashable) -> Any:
        if (result := self.redis.get(key)) is not None:
            return loads(result)
        raise NotCached()

    def _set(self, key: Hashable, result: Any, **kwargs) -> None:
        self.redis.set(key, dumps(result))