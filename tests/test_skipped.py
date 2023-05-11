import sys
import pickle
from tempfile import TemporaryDirectory
from string import Formatter

import f

import pytest


@pytest.mark.skip(reason='It is impossible to do it.')
def test_count_reverse():
    assert 'aaa'.count(f('a')) == 3
    assert 'kkk'.count(f('a')) == 0
    assert 'kkk'.count(f('')) == 4


@pytest.mark.skip(reason='It is impossible to do it.')
def test_dunder_contains_reverse():
    assert f('') in ''
    assert f('') in 'lol'
    assert f('l') in 'lol'
    assert f('lol') in 'lol'
    assert f('lolkek') not in 'lol'


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_replace_reverse():
    # str reference
    assert 'kek'.replace('k', 'f') == 'fef'

    assert 'kek'.replace(f('k'), f('f')) == 'fef'
    assert 'kek'.replace('k', f('f')) == 'fef'
    assert 'kek'.replace(f('k'), 'f') == 'fef'

    assert 'kek'.replace(f('k'), f('f')) == f('fef')
    assert 'kek'.replace('k', f('f')) == f('fef')
    assert 'kek'.replace(f('k'), 'f') == f('fef')


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_center_reverse():
    assert 'banana'.center(20, f('*')) == '*******banana*******'


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_split_reverse():
    assert 'kek'.split(f('e')) == ['k', 'k']


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_rsplit_reverse():
    assert 'kek'.rsplit(f('e')) == ['k', 'k']


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_index_reverse():
    assert 'kek'.index(f('k')) == 0
    assert 'kek'.index(f('e')) == 1


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_rindex_reverse():
    assert 'kek'.rindex(f('k')) == 2
    assert 'kek'.rindex(f('e')) == 1


@pytest.mark.skip(reason='I can\'t change the str class.')
@pytest.mark.skipif(sys.version_info < (3, 9), reason='Requires python3.9, look at documentation: https://docs.python.org/3/library/stdtypes.html#str.removeprefix')
def test_removeprefix_reverse():
    assert 'TestHook'.removeprefix(f('Test')) == 'Hook'
    assert 'BaseTestCase'.removeprefix(f('Test')) == 'BaseTestCase'


@pytest.mark.skip(reason='I can\'t change the str class.')
@pytest.mark.skipif(sys.version_info < (3, 9), reason='Requires python3.9, look at documentation: https://docs.python.org/3/library/stdtypes.html#str.removeprefix')
def test_removesuffix_reverse():
    assert 'TestHook'.removesuffix(f('Hook')) == 'Test'
    assert 'BaseTestCase'.removesuffix(f('Test')) == 'BaseTestCase'


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_join_reverse():
    assert ''.join([f('lol'), f('kek')]) == 'lolkek'
    assert '*'.join([f('lol'), f('kek')]) == 'lol*kek'
    assert '*'.join(['lol', f('kek')]) == 'lol*kek'


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_find_reverse():
    assert 'kek'.find(f('k')) == 0
    assert 'kek'.find(f('e')) == 1
    assert 'kek'.find(f('p')) == -1


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_rfind_reverse():
    assert 'kek'.rfind(f('k')) == 2
    assert 'kek'.rfind(f('e')) == 1
    assert 'kek'.rfind(f('p')) == -1


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_endswith_reverse():
    assert 'kek'.endswith(f('ek'))
    assert 'kek'.endswith(f(''))
    assert not 'kek'.endswith(f('pe'))


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_ljust_reverse():
    assert 'kek'.ljust(5, f('k')) == 'kekkk'


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_rjust_reverse():
    assert 'kek'.rjust(5, f('k')) == 'kkkek'


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_lstrip_reverse():
    assert 'abckek'.lstrip(f('abc')) == 'kek'
    assert '  kek  '.lstrip(f(' ')) == 'kek  '


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_rstrip_reverse():
    assert 'kekabc'.rstrip(f('abc')) == 'kek'
    assert '  kek  '.rstrip(f(' ')) == '  kek'


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_maketrans_reverse():
    assert str.maketrans(f('S'), f('P')) == f('kek').maketrans(f('S'), f('P'))


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_partition_reverse():
    assert 'kek'.partition(f('e')) == ('k', 'e', 'k')
    assert 'kek'.partition(f('i')) == ('kek', '', '')


@pytest.mark.skip(reason='I can\'t change the str class.')
def test_rpartition_reverse():
    assert 'kek'.rpartition(f('e')) == ('k', 'e', 'k')
    assert 'kek'.rpartition(f('i')) == ('', '', 'kek')


@pytest.mark.skip(reason='In MVP i won\'t do it.')
def test_pickle():
    representation = pickle.dumps(f('kek'))
    assert pickle.loads(representation) == 'kek'


@pytest.mark.skip(reason='This is not important - to change the str class.')
def test_str_encode():
    assert isinstance(str.encode(f('kek')), bytes)
    assert str.encode(f('kek')) == b'kek'
    assert str.encode(f('')) == b''


@pytest.mark.skip(reason='This is not important - to change the Formatter class.')
def test_formatter_parse():
    assert ''.join([x[0] for x in Formatter().parse(f('kek'))]) == 'kek'


@pytest.mark.skip(reason="I can't to reproduce this behavior of the str class.")
def test_write_and_read_file():
    with TemporaryDirectory() as directory:
        full_path = os.path.join(directory, 'file.txt')
        with open(full_path, 'w') as file:
            file.write(f('kek'))
        with open(full_path, 'r') as file:
            assert file.read() == 'kek'


@pytest.mark.skip(reason="I can't to reproduce this behavior of the str class.")
def test_open_file():
    with TemporaryDirectory() as directory:
        full_path = f(os.path.join(directory, 'file.txt'))
        with open(full_path, 'w') as file:
            file.write('kek')
        with open(full_path, 'r') as file:
            assert file.read() == 'kek'

    with TemporaryDirectory() as directory:
        full_path = os.path.join(directory, 'file.txt')
        with open(full_path, f('w')) as file:
            file.write('kek')
        with open(full_path, f('r')) as file:
            assert file.read() == 'kek'

    with TemporaryDirectory() as directory:
        full_path = f(os.path.join(directory, 'file.txt'))
        with open(full_path, f('w')) as file:
            file.write('kek')
        with open(full_path, f('r')) as file:
            assert file.read() == 'kek'


@pytest.mark.skip(reason="I can't get the source code from the global scope.")
def test_string_as_variable_when_safe_mode_into_exec():
    with pytest.raises(SyntaxError):
        exec("import f;string = 'kek';f(string)")


@pytest.mark.skip(reason="I can't get the source code from the global scope.")
@pytest.mark.skipif(sys.version_info < (3, 8), reason='Problems with Python 3.7')
def test_string_as_variable_when_safe_mode_into_exec_with_print():
    with pytest.raises(SyntaxError):
        exec("import f;string = 'kek';print(f(string))")
