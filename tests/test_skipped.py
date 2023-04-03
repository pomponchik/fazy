import f

import pytest


@pytest.mark.skip(reason='It is impossible to do it.')
def test_dunder_contains_reverse():
    assert f('') in ''
    assert f('') in 'lol'
    assert f('l') in 'lol'
    assert f('lol') in 'lol'
    assert f('lolkek') not in 'lol'


@pytest.mark.skip(reason='In MVP i won\'t do it.')
def test_pickle():
    representation = pickle.dumps(f('kek'))
    assert pickle.loads(representation) == 'kek'
