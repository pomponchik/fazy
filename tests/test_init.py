import pytest

import f


def test_basic():
    assert f('kek') == 'kek'

def test_empty_string():
    assert f('') == ''

def test_empty_brackets():
    with pytest.raises(SyntaxError):
        f('{}')

def test_number_into_brackets():
    assert str(f('{123}')) == f'{123}'

def test_string_into_brackets():
    assert f('{"kek"}') == f'{"kek"}'
    assert f('{"kek"}') == 'kek'

def test_bool_into_brackets():
    assert f('{"kek"}') == f'{"kek"}'
