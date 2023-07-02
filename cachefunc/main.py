from contextlib import suppress
from functools import wraps
from typing import Any, Callable, Coroutine

from cachefunc.cache.base import BaseCache, NotCached
from cachefunc.cache.dict_cache import DictCache


default_cache = DictCache()


def cachefunc(cache: BaseCache = default_cache, **cache_kwargs,) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with suppress(NotCached):
                return cache.get(func, args, kwargs)
            result = func(*args, **kwargs)
            cache.set(func, args, kwargs, result, **cache_kwargs)
            return result
        return wrapper
    return decorator


def cachecoro(cache: BaseCache = default_cache, **cache_kwargs,) -> Callable:
    def decorator(func: Coroutine) -> Coroutine:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            with suppress(NotCached):
                return cache.get(func, args, kwargs)
            result = await func(*args, **kwargs)
            cache.set(func, args, kwargs, result, **cache_kwargs)
            return result
        return async_wrapper
    return decorator
