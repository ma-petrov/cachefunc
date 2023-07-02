# cachefunc

Caching functions and coroutines result with decorators

# Usage

Basic usage with default dict cache:
```
import aiohttp
import asyncio
import requests
from cachefunc import cachefunc, cachecoro

@cachefunc()
def your_func(url):
    response = requests.get(url)
    return response.text

@cachecoro()
async def your_async_func(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            return html
```

There are two available caches - dict and redis:
```
from cachefunc import cachefunc, DictCache, RedisCache

dict_cache = DictCache()
redis_cache = RedisCache()

@cachefunc(dict_cache)
def your_func_cached_in_dict(url):
    response = requests.get(url)
    return response.text 

@cachefunc(redis_cache)
def your_func_cached_in_redis(url):
    response = requests.get(url)
    return response.text
```

For DictCache it is possible to setup distinct timeout for each function:
```
from datetime import timedelta

@cachefunc(dict_cache, timeout=timedelta(hours=2))
def your_func_cached_for_two_hours(url):
    response = requests.get(url)
    return response.text

@cachefunc(dict_cache, timeout=timedelta(minutes=10))
def your_ohter_func_cached_for_ten_minutes(connection, query):
    cursor = connection.execute(query)
    return cursor.fetchall() 
```

Also custom cache can be created from BaseCache, you should implement
methods _get() and _set():
```
from cachefunc import BaseCache

class CustomCache(BaseCache):
    def _get(self, key: int) -> Any: ...
    def _set(self, key: int, result: Any, **kwargs) -> None: ...
```

## License

[MIT](https://choosealicense.com/licenses/mit/)