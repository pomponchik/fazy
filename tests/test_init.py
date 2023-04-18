import os
import logging
from io import StringIO
from contextlib import redirect_stdout

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
    assert not f.startswith('12345', '124')
    assert f.startswith([1, 2, 3, 4, 5], [1, 2, 3])
    assert not f.startswith([1, 2, 3, 4, 5], [1, 2, 4])


def test_print():
    with redirect_stdout(StringIO()) as context:
        print(f('kek'))

    assert context.getvalue() == 'kek\n'


def test_recursive():
    assert f(f('kek')) == f('kek')
    assert f(f('kek')) == 'kek'


def test_lazy_mode_is_not_implemented():
    with pytest.raises(NotImplementedError):
        f('kek', lazy=False)


def test_lazy_syntax_error():
    with pytest.raises(SyntaxError):
        str(f('{a..}'))


def test_logging():
    class ListHandler(logging.Handler):
        def __init__(self, log_list):
            logging.Handler.__init__(self)
            self.lst = log_list
        def emit(self, record):
            self.lst.append(record)

    lst = []
    logging_handler = ListHandler(lst)
    logging.root.addHandler(logging_handler)

    logging.error(f('kek'))

    assert lst[0].msg == 'kek'
    assert lst[0].message == 'kek'

    assert isinstance(lst[0].msg, type(f('kek')))
    assert type(lst[0].message) is str


def test_logging_to_file():
    file_name = os.path.join('tests', 'data', 'file.log')
    logging.root.addHandler(logging.FileHandler(file_name))

    logging.error(f('kek'))

    with open(file_name, 'r') as file:
        content = file.read()
        assert content == 'kek\n'

    try:
        os.remove(file_name)
    except PermissionError:  # windows oddities
        pass
