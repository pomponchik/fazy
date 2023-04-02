import f


def test_converting_to_bytes():
    assert isinstance(str.encode(f('kek')), bytes)
    assert str.encode(f('kek')) == b'kek'
    assert str.encode(f('')) == b''
