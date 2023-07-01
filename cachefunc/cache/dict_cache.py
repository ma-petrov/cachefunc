from contextlib import suppress
from datetime import datetime, timedelta
from typing import Any, Hashable, Union

from cachefunc.cache.base import BaseCache, NotCached


class DictCache(BaseCache):
    DEFAULT_TIMEOUT = timedelta(hours=1)

    def __init__(self):
        super().__init__()
        self.cache = dict()

    def clear(self) -> None:
        self.cache.clear()

    def _get(self, key: Hashable) -> Any:
        with suppress(KeyError):
            return self.cache[key][0]
        raise NotCached()
    
    def _set(self, key: Hashable, result: Any, **kwargs) -> None:
        timeout = kwargs.get('timeout', self.DEFAULT_TIMEOUT)
        self._clear_expired()
        self.cache[key] = (result, datetime.now() + timeout)

    def _clear_expired(self) -> None:
        now = datetime.now()
        for key, data in self.cache.items():
            if data[1] < now:
                del self.cache[key]
