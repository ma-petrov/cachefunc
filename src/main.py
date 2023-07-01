from collections import namedtuple
from datetime import datetime, timedelta
from functools import wraps
from logging import getLogger
from typing import Any, Callable, Coroutine, Hashable


logger = getLogger(__name__)


DEFAULT_TIMEOUT = timedelta(hours=1)


class BaseCache:
    def __init__(self): ...
    def get(self, key: Hashable) -> Any | None: ...
    def set(self, key: Hashable, data: Any, timeout: timedelta) -> None: ...


class DictCache(BaseCache):
    Row = namedtuple('Row', 'data expiretime')

    def __init__(self):
        self.cache = dict()

    def get(self, key: Hashable) -> Any | None:
        if row := self.cache.get(key):
            return row.data
    
    def set(self, key: Hashable, data: Any, timeout: timedelta) -> None:
        self._clear_expired()
        self.cache[key] = self.Row(data, datetime.now() + timeout)

    def clear(self) -> None:
        self.cache.clear()

    def _clear_expired(self) -> None:
        now = datetime.now()
        for key, row in self.cache.items():
            if row.expiretime < now:
                del self.cache[key]


default_cache = DictCache()


def cachedfunc(
    cache: BaseCache = default_cache,
    timeout: timedelta = DEFAULT_TIMEOUT,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if result := cache.get(func.__name__):
                return result
            result = func(*args, **kwargs)
            cache.set(func.__name__, result, timeout)
            return result
        return wrapper
    return decorator


def cachedcoro(
    cache: BaseCache = default_cache,
    timeout: timedelta = DEFAULT_TIMEOUT,
) -> Callable:
    def decorator(func: Coroutine) -> Coroutine:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            if result := cache.get(func.__name__):
                return result
            result = await func(*args, **kwargs)
            cache.set(func.__name__, result, timeout)
            return result
        return wrapper
    return decorator


