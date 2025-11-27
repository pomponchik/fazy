import logging
import os
from contextlib import redirect_stdout
from io import StringIO

import pytest

import f

GLOBAL_VARIABLE = 'kek'


def test_basic():
    assert f('kek') == 'kek'
    assert f('kek') != 'lol'


def test_basic_capturing_variables():
    kek = 'kek'  # noqa: F841

    assert f('{kek}') == 'kek'
    assert f('{kek}') != 'lol'


def test_basic_capturing_global_variables():
    assert f('{GLOBAL_VARIABLE}') == GLOBAL_VARIABLE
    assert f('{GLOBAL_VARIABLE}') != 'lol'


def test_globals_and_locals_intersection():
    GLOBAL_VARIABLE = 'lol'  # noqa: N806

    assert f('{GLOBAL_VARIABLE}') == 'lol'
    assert f('{GLOBAL_VARIABLE}') == '{0}'.format(GLOBAL_VARIABLE)
    assert f('{GLOBAL_VARIABLE}') == GLOBAL_VARIABLE
    assert f('{GLOBAL_VARIABLE}') != 'kek'


def test_complex_string():
    kek = 'kek?'  # noqa: F841

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
    assert len(accumulator) == 1

    accumulator.pop()

    lazy_string = f('{SomeClass()}')

    assert len(accumulator) == 0

    str(lazy_string)

    assert len(accumulator) == 1

    str(lazy_string)

    assert len(accumulator) == 1


def test_not_lazy():
    number = 5  # noqa: F841

    assert type(f('kek', lazy=False)) is str
    assert type(f('{number}', lazy=False)) is str

    assert f('kek', lazy=False) == 'kek'
    assert f('{number}', lazy=False) == '5'


def test_lazyness_affect():
    changeable = [1, 2, 3]

    not_lazy_string = '{0}'.format(changeable)

    assert not_lazy_string == f('{changeable}')

    lazy_string = f('{changeable}')

    changeable.append(4)

    assert not_lazy_string != lazy_string


def test_lazyness_affect_with_no_lazy_flag():
    changeable = [1, 2, 3]

    not_lazy_string = '{0}'.format(changeable)

    assert not_lazy_string == f('{changeable}')

    lazy_string = f('{changeable}', lazy=False)

    changeable.append(4)

    assert not_lazy_string == lazy_string


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
        kek = 3  # noqa: F841
        return function_2()

    assert function() == '{0}'.format(5)
    assert function() == function_2()

    # comparing with original interpreter behavior:
    def function_3():
        return '{0}'.format(kek)

    def function_4():
        kek = 3  # noqa: F841
        return function_2()

    assert function_3() == '{0}'.format(5)
    assert function_3() == function_4()


def test_builtins():
    assert f('{print}') == '{0}'.format(print)


def test_modules_startswith():
    assert f.startswith('12345', '123')
    assert not f.startswith('12345', '124')
    assert f.startswith([1, 2, 3, 4, 5], [1, 2, 3])
    assert not f.startswith([1, 2, 3, 4, 5], [1, 2, 4])


def test_print():
    with redirect_stdout(StringIO()) as context:
        print(f('kek'))  # noqa: T201

    assert context.getvalue() == 'kek\n'


def test_print_into_exec():
    with redirect_stdout(StringIO()) as context:
        exec("import f;print(f('kek'))")

    assert context.getvalue() == 'kek\n'


def test_recursive():
    assert f(f('kek')) == f('kek')
    assert f(f('kek')) == 'kek'


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
    with open(file_name, 'r') as file:
        content = file.read()
        print(repr(content))


    logging.root.addHandler(logging.FileHandler(file_name))

    with open(file_name, 'r') as file:
        content = file.read()
        print(repr(content))

    logging.error(f('kek'))

    with open(file_name, 'r') as file:
        content = file.read()
        print(repr(content))
        assert content == 'kek\n'

    try:
        os.remove(file_name)
    except PermissionError:  # windows oddities
        pass


def test_list_comprehension():
    assert [f('{x}') for x in range(5)] == ['0', '1', '2', '3', '4']


def test_genexprs():
    assert list((f('{x}') for x in range(5))) == ['0', '1', '2', '3', '4']


def test_not_lazy_mode():
    number = 33  # noqa: F841

    assert f('kek', lazy=False) == 'kek'
    assert f('kek {number}', lazy=False) == 'kek 33'

    assert type(f('kek', lazy=False)) is str
    assert type(f('kek {number}', lazy=False)) is str


def test_no_closures_mode_base_working():
    number = 5  # noqa: F841

    assert f('kek', closures=False) == 'kek'
    assert f('kek {number}', closures=False) == 'kek 5'
    assert f('kek {GLOBAL_VARIABLE}', closures=False) == 'kek kek'


def test_raise_if_closures_when_no_closures_mode():
    number_1 = 5  # noqa: F841

    def wrapper():
        number_2 = 10  # noqa: F841
        def wrapped():
            return f('kek {number_1} {number_2}', closures=False)
        return wrapped

    with pytest.raises(NameError):
        assert wrapper()()


def test_just_simple_exec():
    globals_for_module = {}
    exec('import f; a = f("kek")', globals_for_module)

    assert globals_for_module['a'] == f('kek')
