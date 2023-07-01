from __future__ import annotations


from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Callable, Coroutine, Dict, Hashable, Tuple, Union
from uuid import uuid4

from cachefunc.log import get_logger


logger = get_logger(__name__)


class NotCached(Exception): ...


@dataclass
class FuncCall:
    func: Callable
    func_args: Tuple[Any]
    func_kwargs: Dict[str, Any]

    def __str__(self) -> str:
        return (
            f'{self.func.__qualname__}; '
            f'args: {self.func_args}; '
            f'kwargs {self.func_kwargs}'
        )

    def __eq__(self, other: FuncCall) -> bool:
        return (
            self.func == other.func and
            self.func_args == other.func_args and
            self.func_kwargs == other.func_kwargs
        )


class BaseCache:
    def __init__(self):
        self.__func_call_registry = dict()

    def get(
        self,
        func: Union[Callable, Coroutine],
        func_args: Tuple[Any],
        func_kwargs: Dict[str, Any],
    ) -> None:
        func_call = FuncCall(func, func_args, func_kwargs)
        if key := self._get_key(func_call):
            logger.info(f'Found data in cache for function call: {func_call}')
            return self._get(key)
        raise NotCached

    def set(
        self,
        func: Union[Callable, Coroutine],
        func_args: Tuple[Any],
        func_kwargs: Dict[str, Any],
        result: Any,
        **kwargs,
    ) -> None:
        func_call = FuncCall(func, func_args, func_kwargs)
        logger.info(f'No data was found in cache, call function: {func_call}')
        key = self._set_key(func_call)
        self._set(key, result, **kwargs)

    def _get_key(self, func_call: FuncCall) -> Hashable:
        for key, registered_func_call in self.__func_call_registry.items():
            if func_call == registered_func_call:
                return key
        
    def _set_key(self, func_call: FuncCall) -> Hashable:
        key = uuid4()
        self.__func_call_registry[key] = func_call
        return key

    def _get(self, key: Hashable) -> Any: ...

    def _set(self, key: Hashable, result: Any, **kwargs) -> None: ...
