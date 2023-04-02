import os
import pickle
from io import StringIO
from contextlib import redirect_stdout
from tempfile import TemporaryDirectory

import pytest

import f


GLOBAL_VARIABLE = 'kek'


def test_basic():
    assert f('kek') == 'kek'
    assert f('kek') != 'lol'


def test_basic_capturing_variables():
    kek = 'kek'

    assert f('{kek}') == 'kek'
    assert f('{kek}') != 'lol'


def test_basic_capturing_global_variables():
    assert f('{GLOBAL_VARIABLE}') == GLOBAL_VARIABLE
    assert f('{GLOBAL_VARIABLE}') != 'lol'


def test_globals_and_locals_intersection():
    GLOBAL_VARIABLE = 'lol'

    assert f('{GLOBAL_VARIABLE}') == 'lol'
    assert f('{GLOBAL_VARIABLE}') == '{0}'.format(GLOBAL_VARIABLE)
    assert f('{GLOBAL_VARIABLE}') == GLOBAL_VARIABLE
    assert f('{GLOBAL_VARIABLE}') != 'kek'


def test_complex_string():
    kek = 'kek?'

    assert f('lol {kek} {"cheburek"} {GLOBAL_VARIABLE} {2} {False}') == 'lol kek? cheburek kek 2 False'


def test_empty_string():
    assert f('') == ''
    assert f('') != 'kek'


def test_empty_brackets():
    with pytest.raises(SyntaxError):
        f('{}')


def test_number_into_brackets():
    assert f('{123}') == '{0}'.format(123)
    assert f('{123}') != '{0}'.format(124)


def test_string_into_brackets():
    assert f('{"kek"}') == 'kek'


def test_bool_into_brackets():
    assert f('{False}') == '{0}'.format(False)
    assert f('{True}') == '{0}'.format(True)


def test_lazyness():
    accumulator = []
    class SomeClass:
        def __str__(self):
            accumulator.append('kek')
            return 'kek'

    assert f('{SomeClass()}') == 'kek'
    len(accumulator) == 1

    accumulator.pop()

    some_object = SomeClass()

    lazy_string = f('{SomeClass()}')

    assert len(accumulator) == 0

    str(lazy_string)

    assert len(accumulator) == 1

    str(lazy_string)

    assert len(accumulator) == 1


def test_lazyness_affect():
    changeable = [1, 2, 3]

    not_lazy_string = '{0}'.format(changeable)

    assert not_lazy_string == f('{changeable}')

    lazy_string = f('{changeable}')

    changeable.append(4)

    assert not_lazy_string != lazy_string


def test_str_f():
    assert str(f) == 'f'


def test_repr_f():
    assert repr(f) == 'f'


def test_isinstance_str():
    assert isinstance(f('kek'), str)


def test_read_nonlocal_variable():
    kek = 5

    def function():
        return f('{kek}')

    assert function() == '{0}'.format(kek)


def test_read_nonlocal_variable_difficult():
    kek = 5

    def function_2():
        return f('{kek}')

    def function():
        return function_2()

    assert function() == '{0}'.format(kek)


def test_read_nonlocal_variable_nested():
    kek = 5

    def function_2():
        return f('{kek}')

    def function():
        kek = 3
        return function_2()

    assert function() == '{0}'.format(5)

    # comparing with original interpreter behavior:
    def function_2():
        return '{0}'.format(kek)

    def function():
        kek = 3
        return function_2()

    assert function() == '{0}'.format(5)


def test_builtins():
    assert f('{print}') == '{0}'.format(print)


def test_modules_startswith():
    assert f.startswith('12345', '123')
    assert f.startswith([1, 2, 3, 4, 5], [1, 2, 3])
    assert not f.startswith([1, 2, 3, 4, 5], [1, 2, 4])


def test_print():
    with redirect_stdout(StringIO()) as context:
        print(f('kek'))

    assert context.getvalue() == 'kek\n'


def test_write_and_read_file():
    with TemporaryDirectory() as directory:
        full_path = os.path.join(directory, 'file.txt')
        with open(full_path, 'w') as file:
            file.write(f('kek'))
        with open(full_path, 'r') as file:
            assert file.read() == 'kek'


def test_pickle():
    representation = pickle.dumps(f('kek'))
    assert pickle.loads(representation) == 'kek'
