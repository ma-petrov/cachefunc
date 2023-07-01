from unittest.mock import MagicMock, call
from cachedfunc.main import cachedfunc, default_cache


RESULT = 'some data'
OTHER_RESULT = 'other result'


@cachedfunc()
def target_func(testcall: MagicMock) -> str:
    testcall('target func was called')
    return RESULT


@cachedfunc()
def other_target_func(testcall: MagicMock) -> str:
    testcall('other target func was called')
    return OTHER_RESULT


class A:
    @cachedfunc()
    def target_func(self, testcall: MagicMock) -> str:
        testcall('method of A was called')
        return RESULT

class B:
    @cachedfunc()
    def target_func(self, testcall: MagicMock) -> str:
        testcall('method of B was called')
        return OTHER_RESULT
    

def test_cachedfunc__no_data_in_cache():
    default_cache.clear()
    testcall = MagicMock()

    result = target_func(testcall)
    testcall.assert_called_once_with('target func was called')
    assert result == RESULT


def test_cachedfunc__fetch_data_from_cache():
    default_cache.clear()
    testcall = MagicMock()

    result = target_func(testcall)
    result = target_func(testcall)
    testcall.assert_called_once_with('target func was called')
    assert result == RESULT
    

def test_cachedfunc__unique_key():
    default_cache.clear()
    testcall = MagicMock()

    result = target_func(testcall)
    other_result = other_target_func(testcall)
    testcall.assert_has_calls([
        call('target func was called'),
        call('other target func was called'),
    ])
    assert result == RESULT
    assert other_result == OTHER_RESULT
    

def test_cachedfunc__unique_key_class_method():
    default_cache.clear()
    testcall = MagicMock()

    result = A().target_func(testcall)
    other_result = B().target_func(testcall)
    testcall.assert_has_calls([
        call('method of A was called'),
        call('method of B was called'),
    ])
    assert result == RESULT
    assert other_result == OTHER_RESULT


