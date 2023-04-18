import sys

import pytest

import f


def test_encode():
    assert isinstance(f('kek').encode(), bytes)
    assert f('kek').encode() == b'kek'
    assert f('kek').encode(encoding='UTF-8', errors='strict') == b'kek'
    assert f('kek').encode(encoding=f('UTF-8'), errors=f('strict')) == b'kek'
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
    assert f('1,2,3').split(',', maxsplit=1) == ['1', '2,3']


def test_rsplit():
    assert f('kek').rsplit('e') == ['k', 'k']
    assert f('kek').rsplit(f('e')) == ['k', 'k']
    assert f('k k').rsplit() == ['k', 'k']
    assert f('1,2,3').rsplit(',', maxsplit=1) == ['1,2', '3']


def test_splitlines():
    assert f('kek').splitlines() == ['kek']
    assert f('kek\n').splitlines() == ['kek']
    assert f('lol\nkek\n').splitlines() == ['lol', 'kek']
    assert f('kek\n').splitlines() == ['kek']
    assert f('lol\nkek\n').splitlines(keepends=True) == ['lol\n', 'kek\n']
    assert f('kek\n').splitlines(keepends=True) == ['kek\n']


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


def test_rfind():
    # str references
    assert 'kek'.rfind('k') == 2
    assert 'kek'.rfind('e') == 1
    assert 'kek'.rfind('p') == -1

    assert f('kek').rfind('k') == 2
    assert f('kek').rfind(f('k')) == 2

    assert f('kek').rfind('e') == 1
    assert f('kek').rfind(f('e')) == 1

    assert f('kek').rfind('p') == -1
    assert f('kek').rfind(f('p')) == -1

    with pytest.raises(TypeError):
        f('kek').rfind(0)


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


def test_rindex():
    # str references
    assert 'kek'.rindex('k') == 2
    assert 'kek'.rindex('e') == 1
    with pytest.raises(ValueError):
        'kek'.rindex('p') == -1

    assert f('kek').rindex('k') == 2
    assert f('kek').rindex(f('k')) == 2

    assert f('kek').rindex('e') == 1
    assert f('kek').rindex(f('e')) == 1

    with pytest.raises(ValueError):
        f('kek').rindex('p')
    with pytest.raises(ValueError):
        f('kek').rindex(f('p'))
    with pytest.raises(TypeError):
        f('kek').rindex(0)


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


def test_isalnum():
    # str references
    assert 'kek'.isalnum()
    assert 'kek55'.isalnum()
    assert '55'.isalnum()
    assert not ''.isalnum()
    assert not 'kek55 lol 66'.isalnum()

    assert f('kek').isalnum()
    assert f('kek55').isalnum()
    assert f('55').isalnum()
    assert not f('').isalnum()
    assert not f('kek55 lol 66').isalnum()


def test_isalpha():
    # str references
    assert 'kek'.isalpha()
    assert 'Kek'.isalpha()
    assert not ''.isalpha()
    assert not '*'.isalpha()
    assert not ' '.isalpha()
    assert not '55'.isalpha()

    assert f('kek').isalpha()
    assert f('Kek').isalpha()
    assert not f('').isalpha()
    assert not f('*').isalpha()
    assert not f(' ').isalpha()
    assert not f('55').isalpha()


def test_isdecimal():
    # str references
    assert '0'.isdecimal()
    assert '55'.isdecimal()
    assert not '-55'.isdecimal()
    assert not ''.isdecimal()
    assert not 'kek'.isdecimal()
    assert not '1A'.isdecimal()

    assert f('0').isdecimal()
    assert f('55').isdecimal()
    assert not f('-55').isdecimal()
    assert not f('').isdecimal()
    assert not f('kek').isdecimal()
    assert not f('1A').isdecimal()


def test_isnumeric():
    # str references
    assert '0'.isnumeric()
    assert '55'.isnumeric()
    assert not '-55'.isnumeric()
    assert not ''.isnumeric()
    assert not 'kek'.isnumeric()
    assert not '1A'.isnumeric()

    assert '\u0030'.isnumeric()
    assert '\u00B2'.isnumeric()

    assert f('0').isnumeric()
    assert f('55').isnumeric()
    assert not f('-55').isnumeric()
    assert not f('').isnumeric()
    assert not f('kek').isnumeric()
    assert not f('1A').isnumeric()

    assert f('\u0030').isnumeric()
    assert f('\u00B2').isnumeric()


def test_isspace():
    assert f(' ').isspace()
    assert f('\n').isspace()
    assert f('\t').isspace()

    assert not f('kek').isspace()
    assert not f('k e k').isspace()
    assert not f('').isspace()


def test_isprintable():
    assert f('').isprintable()
    assert f('kek').isprintable()

    assert not f('\n').isprintable()


def test_isidentifier():
    assert f('kek').isidentifier()
    assert f('kek8').isidentifier()
    assert f('lol_kek').isidentifier()
    assert f('lol_kek_8').isidentifier()
    assert not f('').isidentifier()
    assert not f(' ').isidentifier()
    assert not f('\n').isidentifier()
    assert not f('\nkek').isidentifier()
    assert not f('lol-kek-8').isidentifier()


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


def test_casefold():
    assert f('').casefold() == ''
    assert f('ß').casefold() == 'ss'
    assert f('KEK').casefold() == 'kek'


def test_expandtabs():
    assert f('01\t012\t0123\t01234').expandtabs() == '01\t012\t0123\t01234'.expandtabs()
    assert f('01\t012\t0123\t01234').expandtabs(4) == '01\t012\t0123\t01234'.expandtabs(4)
    assert f('').expandtabs(4) == ''.expandtabs(4)


def test_istitle():
    assert f('Kek').istitle()
    assert f('   Kek').istitle()
    assert not f('').istitle()
    assert not f('KEK').istitle()
    assert not f('kek').istitle()
    assert not f('   kek').istitle()


@pytest.mark.skipif(sys.version_info < (3, 9), reason='Requires python3.9, look at documentation: https://docs.python.org/3/library/stdtypes.html#str.removeprefix')
def test_removeprefix():
    # str references
    assert 'TestHook'.removeprefix('Test') == 'Hook'
    assert 'BaseTestCase'.removeprefix('Test') == 'BaseTestCase'

    assert f('TestHook').removeprefix('Test') == 'Hook'
    assert f('BaseTestCase').removeprefix('Test') == 'BaseTestCase'

    assert f('TestHook').removeprefix(f('Test')) == 'Hook'
    assert f('BaseTestCase').removeprefix(f('Test')) == 'BaseTestCase'


@pytest.mark.skipif(sys.version_info < (3, 9), reason='Requires python3.9, look at documentation: https://docs.python.org/3/library/stdtypes.html#str.removeprefix')
def test_removesuffix():
    # str references
    assert 'TestHook'.removesuffix('Hook') == 'Test'
    assert 'BaseTestCase'.removesuffix('Test') == 'BaseTestCase'

    assert f('TestHook').removesuffix('Hook') == 'Test'
    assert f('BaseTestCase').removesuffix('Test') == 'BaseTestCase'

    assert f('TestHook').removesuffix(f('Hook')) == 'Test'
    assert f('BaseTestCase').removesuffix(f('Test')) == 'BaseTestCase'


def test_lstrip():
    assert f('  kek  ').lstrip() == 'kek  '
    assert f('kek').lstrip() == 'kek'
    assert f('kek  ').lstrip() == 'kek  '
    assert f('abckek').lstrip('abc') == 'kek'
    assert f('ccckek').lstrip('c') == 'kek'
    assert f('abckek').lstrip(f('abc')) == 'kek'
    assert f('kek  ').lstrip(' ') == 'kek  '
    assert f('kek  ').lstrip(f(' ')) == 'kek  '


def test_rstrip():
    assert f('  kek  ').rstrip() == '  kek'
    assert f('kek').rstrip() == 'kek'
    assert f('  kek').rstrip() == '  kek'
    assert f('kekabc').rstrip('abc') == 'kek'
    assert f('kekccc').rstrip('c') == 'kek'
    assert f('kekabc').rstrip(f('abc')) == 'kek'
    assert f('  kek').rstrip(' ') == '  kek'
    assert f('  kek').rstrip(f(' ')) == '  kek'


def test_ljust():
    assert f('kek').ljust(5) == 'kek  '
    assert f('kek').ljust(5, 'k') == 'kekkk'
    assert f('kek').ljust(5, f('k')) == 'kekkk'


def test_rjust():
    assert f('kek').rjust(5) == '  kek'
    assert f('kek').rjust(5, 'k') == 'kkkek'
    assert f('kek').rjust(5, f('k')) == 'kkkek'


def test_maketrans():
    assert f('kek').maketrans({}) == {}
    assert str.maketrans('mSa', 'eJo', 'odnght') == f('kek').maketrans('mSa', 'eJo', 'odnght')
    assert str.maketrans('mSa', 'eJo', 'odnght') == f('kek').maketrans(f('mSa'), f('eJo'), f('odnght'))
    assert str.maketrans('S', 'P') == f('kek').maketrans('S', 'P')
    assert str.maketrans('S', 'P') == f('kek').maketrans(f('S'), f('P'))


def test_partition():
    assert f('kek').partition('e') == ('k', 'e', 'k')
    assert f('kek').partition('i') == ('kek', '', '')
    assert f('kek').partition(f('e')) == ('k', 'e', 'k')


def test_rpartition():
    assert f('kek').rpartition('e') == ('k', 'e', 'k')
    assert f('kek').rpartition('i') == ('', '', 'kek')
    assert f('kek').rpartition(f('e')) == ('k', 'e', 'k')


def test_swapcase():
    assert f('kek').swapcase() == 'KEK'
    assert f('KEK').swapcase() == 'kek'
    assert f('KeK').swapcase() == 'kEk'
