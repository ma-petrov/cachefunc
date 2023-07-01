from unittest.mock import MagicMock, call
from cachefunc.main import cachefunc, default_cache


RESULT = 'some data'
OTHER_RESULT = 'other result'


@cachefunc()
def target_func(testcall: MagicMock) -> str:
    testcall('target func was called')
    return RESULT


@cachefunc()
def other_target_func(testcall: MagicMock) -> str:
    testcall('other target func was called')
    return OTHER_RESULT


@cachefunc()
def target_func_with_args(testcall: MagicMock, arg: int) -> str:
    testcall(f'called with arg: {arg}')
    return arg


class A:
    @cachefunc()
    def target_func(self, testcall: MagicMock) -> str:
        testcall('method of A was called')
        return RESULT

class B:
    @cachefunc()
    def target_func(self, testcall: MagicMock) -> str:
        testcall('method of B was called')
        return OTHER_RESULT


def test_cachefunc__fetch_data_from_cache():
    default_cache.clear()
    testcall = MagicMock()

    assert target_func(testcall) == RESULT
    assert target_func(testcall) == RESULT
    testcall.assert_called_once_with('target func was called')
    

def test_cachefunc__unique_key():
    default_cache.clear()
    testcall = MagicMock()

    assert target_func(testcall) == RESULT
    assert other_target_func(testcall) == OTHER_RESULT
    testcall.assert_has_calls([
        call('target func was called'),
        call('other target func was called'),
    ])
    

def test_cachefunc__unique_key_class_method():
    default_cache.clear()
    testcall = MagicMock()

    assert A().target_func(testcall) == RESULT
    assert B().target_func(testcall) == OTHER_RESULT
    testcall.assert_has_calls([
        call('method of A was called'),
        call('method of B was called'),
    ])
    

def test_cachefunc__distinct_arg_cache():
    default_cache.clear()
    testcall = MagicMock()

    assert target_func_with_args(testcall, 1) == 1
    assert target_func_with_args(testcall, 1) == 1
    assert target_func_with_args(testcall, 2) == 2
    assert target_func_with_args(testcall, 2) == 2
    testcall.assert_has_calls([
        call('called with arg: 1'),
        call('called with arg: 2'),
    ])
