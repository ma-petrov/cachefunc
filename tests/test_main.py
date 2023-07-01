from datetime import timedelta
from unittest.mock import MagicMock
from src.main import cachedfunc, default_cache


RESULT = 'some data'


@cachedfunc()
def target_func(testcall: MagicMock) -> str:
    testcall('target func was called')
    return RESULT
    

def test_cachedfunc__no_data_in_cache():
    default_cache.clear()
    testcall = MagicMock()
    result = target_func(testcall)
    testcall.assert_called_once_with('target func was called')
    assert result == RESULT


def test_cachedfunc__fetch_data_from_cache():
    default_cache.set(target_func.__name__, RESULT, timeout=timedelta(hours=1))
    testcall = MagicMock()
    result = target_func(testcall)
    testcall.assert_not_called()
    assert result == RESULT
    

def test_cachedfunc__called_only_once():
    default_cache.clear()
    testcall = MagicMock()
    result = target_func(testcall)
    result = target_func(testcall)
    testcall.assert_called_once_with('target func was called')
    assert result == RESULT