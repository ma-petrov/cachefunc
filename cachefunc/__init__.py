from cachefunc.cache.base import BaseCache
from cachefunc.cache.dict_cache import DictCache
from cachefunc.cache.redis_cache import RedisCache
from cachefunc.main import (
    default_cache,
    cachefunc,
    cachecoro,
)