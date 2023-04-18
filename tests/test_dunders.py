import sys

import pytest

import f


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

    assert lazy_string == lazy_string
    assert f('kek') == f('kek')

    assert lazy_string == 'kek'
    assert lazy_string != 'no kek'

    assert 'kek' == lazy_string
    assert 'no kek' != lazy_string

    assert f('e') == 'e'
    assert 'e' == f('e')


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
    assert len(f('')) == 0


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
    assert ''.join([x for x in f('1234')]) == '1234'
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
    assert f('*') * 0 == f('')
    assert f('*') * 2 == f('**')
    assert f('*') * 10 == f('**********')

    assert f('*') * 0 != f('kek')
    assert f('*') * 2 != f('*')
    assert f('*') * 10 != f('*')


def test_dunder_rmul():
    assert 2 * f('*') == f('**')


def test_dunder_reduce():
    # an str reference
    with pytest.raises(TypeError):
        'kek'.__reduce__()

    with pytest.raises(TypeError):
        f('kek').__reduce__()


def test_dunder_setattr():
    # an str reference
    with pytest.raises(AttributeError):
        ''.kek = 'kek'

    with pytest.raises(AttributeError):
        f('').kek = 'kek'


def test_dunder_sizeof():
    assert isinstance(sys.getsizeof(f('kek')), int)
    assert sys.getsizeof(f('kek')) > sys.getsizeof('kek')
