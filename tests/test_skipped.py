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


@pytest.mark.skip(reason='I can\'t change the str slass.')
def test_replace_reverse():
    # str reference
    assert 'kek'.replace('k', 'f') == 'fef'

    assert 'kek'.replace(f('k'), f('f')) == 'fef'
    assert 'kek'.replace('k', f('f')) == 'fef'
    assert 'kek'.replace(f('k'), 'f') == 'fef'

    assert 'kek'.replace(f('k'), f('f')) == f('fef')
    assert 'kek'.replace('k', f('f')) == f('fef')
    assert 'kek'.replace(f('k'), 'f') == f('fef')


@pytest.mark.skip(reason='I can\'t change the str slass.')
def test_split_reverse():
    assert 'kek'.split(f('e')) == ['k', 'k']
    assert 'k k'.split() == ['k', 'k']


@pytest.mark.skip(reason='I can\'t change the str slass.')
def test_find_reverse():
    assert 'kek'.find(f('k')) == 0
    assert 'kek'.find(f('e')) == 1
    assert 'kek'.find(f('p')) == -1


@pytest.mark.skip(reason='I can\'t change the str slass.')
def test_endswith_reverse():
    assert 'kek'.endswith(f('ek'))
    assert 'kek'.endswith(f(''))
    assert not 'kek'.endswith(f('pe'))


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
