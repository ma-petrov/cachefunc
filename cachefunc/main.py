from base64 import b64encode
from collections import namedtuple
from contextlib import suppress
from datetime import datetime, timedelta
from functools import wraps
from logging import getLogger
from typing import Any, Callable, Coroutine, Hashable, Union


logger = getLogger(__name__)


DEFAULT_TIMEOUT = timedelta(hours=1)


class BaseCache:
    class NotCached(Exception): ...
    def __init__(self): ...
    def get(self, key: Hashable) -> Union[Any, None]: ...
    def set(self, key: Hashable, data: Any, timeout: timedelta) -> None: ...


class DictCache(BaseCache):
    Row = namedtuple('Row', 'data expiretime')

    def __init__(self):
        self.cache = dict()

    def get(self, key: Hashable) -> Union[Any, None]:
        with suppress(KeyError):
            return self.cache[key].data
        raise BaseCache.NotCached()
    
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


def _get_key(func: Union[Callable, Coroutine]) -> str:
    return func.__qualname__


def cachefunc(
    cache: BaseCache = default_cache,
    timeout: timedelta = DEFAULT_TIMEOUT,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        key = _get_key(func)
        print(key)
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with suppress(BaseCache.NotCached):
                return cache.get(key)
            result = func(*args, **kwargs)
            cache.set(key, result, timeout)
            return result
        return wrapper
    return decorator


def cachecoro(
    cache: BaseCache = default_cache,
    timeout: timedelta = DEFAULT_TIMEOUT,
) -> Callable:
    def decorator(func: Coroutine) -> Coroutine:
        key = _get_key(func)
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            with suppress(BaseCache.NotCached):
                return cache.get(key)
            result = await func(*args, **kwargs)
            cache.set(key, result, timeout)
            return result
        return async_wrapper
    return decorator


