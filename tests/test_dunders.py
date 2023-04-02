import pytest

import f

['__reduce__', '__reduce_ex__', '__rmul__', '__setattr__', '__sizeof__', '__subclasshook__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'removeprefix', 'removesuffix', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']

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

    assert 'kek' == lazy_string
    assert 'no kek' != lazy_string


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


def test_dunder_len():
    kek = '1234567890'

    assert len(f('lol')) == 3
    assert len(f('{kek}')) == 10


def test_dunder_dir():
    assert isinstance(dir(f('lol')), list)


def test_dunder_getitem():
    assert f('1234')[0] == '1'
    assert f('1234')[1] == '2'
    assert f('1234')[2] == '3'
    assert f('1234')[3] == '4'


def test_dunder_getitem_exceptions():
    with pytest.raises(IndexError):
        f('1234')[5]
    with pytest.raises(TypeError):
        f('1234')['5']


def test_dunder_getnewargs():
    assert len(f('1234').__getnewargs__()) == 5
    assert len(f('').__getnewargs__()) == 5
    assert isinstance(f('1234').__getnewargs__(), type(''.__getnewargs__()))


def test_dunder_ge():
    assert '1234' >= '123'
    assert f('1234') >= '123'
    assert f('1234') >= f('123')
    assert '1234' >= f('123')

    assert '1234' >= '1234'
    assert f('1234') >= '1234'
    assert f('1234') >= f('1234')
    assert '1234' >= f('1234')

    assert not ('1234' >= '12345')
    assert not (f('1234') >= '12345')
    assert not (f('1234') >= f('12345'))
    assert not ('1234' >= f('12345'))

    with pytest.raises(TypeError):
        f('1234') >= 12345


def test_dunder_gt():
    assert '1234' > '123'
    assert f('1234') > '123'
    assert f('1234') > f('123')
    assert '1234' > f('123')

    assert not ('1234' > '1234')
    assert not (f('1234') > '1234')
    assert not (f('1234') > f('1234'))
    assert not ('1234' > f('1234'))

    assert not ('1234' > '12345')
    assert not (f('1234') > '12345')
    assert not (f('1234') > f('12345'))
    assert not ('1234' > f('12345'))

    with pytest.raises(TypeError):
        f('1234') > 12345


def test_dunder_le():
    assert '123' <= '1234'
    assert f('123') <= '1234'
    assert f('123') <= f('1234')
    assert '123' <= f('1234')

    assert '1234' <= '1234'
    assert f('1234') <= '1234'
    assert f('1234') <= f('1234')
    assert '1234' <= f('1234')

    assert not ('12345' <= '1234')
    assert not (f('12345') <= '1234')
    assert not (f('12345') <= f('1234'))
    assert not ('12345' <= f('1234'))

    with pytest.raises(TypeError):
        f('1234') <= 12345


def test_dunder_lt():
    assert '123' < '1234'
    assert f('123') < '1234'
    assert f('123') < f('1234')
    assert '123' < f('1234')

    assert not ('12345' < '1234')
    assert not (f('12345') < '1234')
    assert not (f('12345') < f('1234'))
    assert not ('12345' < f('1234'))

    with pytest.raises(TypeError):
        f('1234') < 12345


def test_dunder_ne():
    assert '123' != '1234'
    assert f('123') != '1234'
    assert f('123') != f('1234')
    assert '123' != f('1234')

    assert not ('1234' != '1234')
    assert not (f('1234') != '1234')
    assert not (f('1234') != f('1234'))
    assert not ('1234' != f('1234'))

    assert f('1234') != 1234
    assert 1234 != f('1234')


def test_dunder_hash():
    assert isinstance(hash(f('1234')), int)


def test_dunder_iter():
    assert ''.join([x for x in f('1234')]) == f('1234')
    assert ''.join([x for x in f('{1234}')]) == f('1234')
    assert ''.join([x for x in f('')]) == f('')


def test_dunder_mod():
    assert f('1234 %s') % '1234' == f('1234 1234')
    assert f('1234 %s') % f('1234') == f('1234 1234')

    assert f('%s %s') % (f('1234'), f('1234')) == f('1234 1234')
    assert f('%s %s') % ('1234', f('1234')) == f('1234 1234')
    assert f('%s %s') % ('1234', '1234') == f('1234 1234')
    assert f('%s %s') % (f('1234'), '1234') == f('1234 1234')


def test_str_dunder_rmod():
    assert '1234 %s' % f('1234') == f('1234 1234')
    assert '%s %s' % (f('1234'), f('1234')) == f('1234 1234')

    assert f('1234 %s') % f('1234') == f('1234 1234')
    assert f('%s %s') % (f('1234'), f('1234')) == f('1234 1234')


def test_dunder_mul():
    assert f('*') * 2 == f('**')
    assert f('*') * 10 == f('**********')


def test_dunder_reduce():
    with pytest.raises(TypeError):
        'kek'.__reduce__()
    with pytest.raises(TypeError):
        f('kek').__reduce__()
