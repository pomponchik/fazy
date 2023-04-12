import sys

import pytest

import f


def test_encode():
    assert isinstance(f('kek').encode(), bytes)
    assert f('kek').encode() == b'kek'
    assert f('').encode() == b''
    assert f('{123}').encode() == b'123'


def test_replace():
    assert f('kek').replace('k', 'f') == 'fef'
    assert f('kek').replace(f('k'), 'f') == 'fef'
    assert f('kek').replace('k', f('f')) == 'fef'
    assert f('kek').replace(f('k'), f('f')) == 'fef'

    assert f('kek').replace('k', 'f') == f('fef')
    assert f('kek').replace(f('k'), 'f') == f('fef')
    assert f('kek').replace('k', f('f')) == f('fef')
    assert f('kek').replace(f('k'), f('f')) == f('fef')


def test_split():
    assert f('kek').split('e') == ['k', 'k']
    assert f('kek').split(f('e')) == ['k', 'k']
    assert f('k k').split() == ['k', 'k']


def test_find():
    # str references
    assert 'kek'.find('k') == 0
    assert 'kek'.find('e') == 1
    assert 'kek'.find('p') == -1

    assert f('kek').find('k') == 0
    assert f('kek').find(f('k')) == 0

    assert f('kek').find('e') == 1
    assert f('kek').find(f('e')) == 1

    assert f('kek').find('p') == -1
    assert f('kek').find(f('p')) == -1

    with pytest.raises(TypeError):
        f('kek').find(0)


def test_index():
    # str references
    assert 'kek'.index('k') == 0
    assert 'kek'.index('e') == 1
    with pytest.raises(ValueError):
        'kek'.index('p') == -1

    assert f('kek').index('k') == 0
    assert f('kek').index(f('k')) == 0

    assert f('kek').index('e') == 1
    assert f('kek').index(f('e')) == 1

    with pytest.raises(ValueError):
        f('kek').index('p')
    with pytest.raises(ValueError):
        f('kek').index(f('p'))
    with pytest.raises(TypeError):
        f('kek').index(0)


@pytest.mark.skipif(sys.version_info < (3, 7), reason='Requires python3.7, look at documentation: https://docs.python.org/3/library/stdtypes.html#str.isascii')
def test_isascii():
    assert f('kek').isascii() == True
    assert f('кек').isascii() == False


def test_isupper():
    assert f('BANANA').isupper()
    assert not f('banana').isupper()
    assert not f('baNana').isupper()
    assert not f(' ').isupper()
    assert not f('').isupper()


def test_islower():
    assert not f('BANANA').islower()
    assert f('banana').islower()
    assert not f('baNana').islower()
    assert not f(' ').islower()
    assert not f('').islower()


def test_upper():
    assert f('BANANA').upper() == 'BANANA'
    assert f('banana').upper() == 'BANANA'
    assert f('baNana').upper() == 'BANANA'
    assert f('').upper() == ''
    assert f(' ').upper() == ' '


def test_lower():
    assert f('BANANA').lower() == 'banana'
    assert f('banana').lower() == 'banana'
    assert f('baNana').lower() == 'banana'
    assert f('').lower() == ''
    assert f(' ').lower() == ' '


def test_zfill():
    assert f('42').zfill(5) == '00042'
    assert f('-42').zfill(5) == '-0042'
    assert f('').zfill(5) == '00000'


def test_count():
    assert f('aaa').count('a') == 3
    assert f('kkk').count('a') == 0
    assert f('kkk').count('') == 4

    assert f('aaa').count(f('a')) == 3
    assert f('kkk').count(f('a')) == 0
    assert f('kkk').count(f('')) == 4


def test_translate():
    # an str reference
    assert 'aaa'.translate({97: 98}) == 'bbb'

    assert f('aaa').translate({97: 98}) == 'bbb'


def test_title():
    # str references
    assert 'kek'.title() == 'Kek'
    assert 'lol kek'.title() == 'Lol Kek'

    assert f('kek').title() == 'Kek'
    assert f('lol kek').title() == 'Lol Kek'


def test_format():
    assert f('kek').format() == 'kek'
    assert '{0}'.format(f('kek')) == 'kek'


def test_startswith():
    # str references
    assert 'kek'.startswith('ke')
    assert 'kek'.startswith('')
    assert not 'kek'.startswith('pe')

    assert f('kek').startswith('ke')
    assert f('kek').startswith('')
    assert not f('kek').startswith('pe')

    assert f('kek').startswith(f('ke'))
    assert f('kek').startswith(f(''))
    assert not f('kek').startswith(f('pe'))


def test_endswith():
    # str references
    assert 'kek'.endswith('ek')
    assert 'kek'.endswith('')
    assert not 'kek'.endswith('pe')

    assert f('kek').endswith('ek')
    assert f('kek').endswith('')
    assert not f('kek').endswith('pe')

    assert f('kek').endswith(f('ek'))
    assert f('kek').endswith(f(''))
    assert not f('kek').endswith(f('pe'))


def test_isdigit():
    assert f('888').isdigit()
    assert f('0').isdigit()
    assert f('0001').isdigit()
    assert not f('8.0').isdigit()
    assert not f('-8').isdigit()
    assert not f('kek').isdigit()
    assert not f('09 kek').isdigit()


def test_center():
    # str references
    assert 'banana'.center(20) == '       banana       '
    assert 'banana'.center(2) == 'banana'
    assert 'banana'.center(20, '*') == '*******banana*******'

    assert f('banana').center(20) == '       banana       '
    assert f('banana').center(2) == 'banana'
    assert f('banana').center(20, '*') == '*******banana*******'
    assert f('banana').center(20, f('*')) == '*******banana*******'


def test_join():
    # str references
    assert ''.join(['lol', 'kek']) == 'lolkek'
    assert '*'.join(['lol', 'kek']) == 'lol*kek'

    assert f('').join(['lol', 'kek']) == 'lolkek'
    assert f('*').join(['lol', 'kek']) == 'lol*kek'

    assert f('').join([f('lol'), f('kek')]) == 'lolkek'
    assert f('*').join([f('lol'), f('kek')]) == 'lol*kek'


def test_capitalize():
    assert ''.capitalize() == ''
    assert 'kek'.capitalize() == 'Kek'

    assert f('').capitalize() == ''
    assert f('kek').capitalize() == 'Kek'
