from __future__ import annotations


from dataclasses import dataclass
from typing import Any, Callable, Coroutine, Dict, Tuple, Union
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
    
    def to_key(self) -> int:
        return hash(
            self.func.__qualname__ +
            ''.join(str(id(v)) for v in self.func_args) +
            ''.join(str(id(v)) for v in self.func_kwargs.values())
        )


class BaseCache:
    def get(
        self,
        func: Union[Callable, Coroutine],
        func_args: Tuple[Any],
        func_kwargs: Dict[str, Any],
    ) -> None:
        func_call = FuncCall(func, func_args, func_kwargs)
        key = func_call.to_key()
        result = self._get(key)
        logger.info(f'Found data in cache for function call: {func_call}')
        return result

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
        key = func_call.to_key()
        self._set(key, result, **kwargs)

    def _get(self, key: int) -> Any: ...

    def _set(self, key: int, result: Any, **kwargs) -> None: ...
