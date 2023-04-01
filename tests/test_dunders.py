import pytest

import f

['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'removeprefix', 'removesuffix', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']

def test_dunder_str():
    lazy_string = f('kek')

    assert isinstance(str(lazy_string), str)
    assert str(lazy_string) == 'kek'


def test_dunder_repr():
    lazy_string = f('kek')

    assert isinstance(repr(lazy_string), str)
    assert repr(lazy_string) == "'kek'"


def test_dunder_eq():
    lazy_string = f('kek')

    assert lazy_string == 'kek'
    assert lazy_string != 'no kek'


def test_dunder_add_and_radd():
    assert f('lol') + f('kek') == f('lolkek')
    assert f('lol') + f('kek') == 'lolkek'
    assert f('lol') + 'kek' == 'lolkek'
    assert 'lol' + f('kek') == 'lolkek'
    assert 'lol' + f('kek') == f('lolkek')
    assert f('lol') + 'kek' == f('lolkek')

    assert f('lol') + f('kek') != f('not lolkek')

    with pytest.raises(TypeError):
        f('lol') + 5

    try:
        f('lol') + 5
    except TypeError as e:
        assert str(e) == 'can only concatenate str (not "int") to str'


def test_dunder_contains():
    assert 'l' in f('lol')
    assert 'lol' in f('lol')

    assert 'lolkek' not in f('lol')

    assert f('l') in f('lol')
    assert f('lol') in f('lol')

    assert f('lolkek') not in f('lol')


@pytest.mark.skip(reason='It is impossible to do it.')
def test_dunder_contains_reverce():
    assert f('l') in 'lol'
    assert f('lol') in 'lol'
    assert f('lolkek') not in 'lol'


def test_dunder_len():
    kek = '1234567890'

    assert len(f('lol')) == 3
    assert len(f('{kek}')) == 10
