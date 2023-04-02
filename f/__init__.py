import gc
import sys
import inspect
from functools import wraps
from string import Formatter
from collections import UserString


class ChainUnit:
    def __init__(self, base, appendix=None, lazy=True):
        self.base = base
        self.appendix = appendix
        if self.appendix is not None:
            if self.appendix == '':
                raise SyntaxError('lazy f-string: empty expression not allowed')


class LazyString(UserString, str):
    def __init__(self, units, local_locals, local_globals, local_nonlocals, lazy):
        self.units = units
        self.local_locals = local_locals
        self.local_globals = local_globals
        self.local_nonlocals = local_nonlocals
        self.lazy = lazy
        self.result = None

    def __new__(cls, *args, **kwargs):
        return str.__new__(cls)

    def __add__(self, other):
        if isinstance(other, type(self)):
            other = other.data
        return self.data.__add__(other)

    def __radd__(self, other):
        if isinstance(other, type(self)):
            other = other.data
        if not isinstance(other, str):
            raise TypeError('can only concatenate str (not "{0}") to str'.format(type(other).__name__))

        return other + self.data

    def __getitem__(self, index):
        return self.data.__getitem__(index)

    def __getnewargs__(self):
        return (self.units, self.local_locals, self.local_globals, self.local_nonlocals, self.lazy)

    def __mod__(self, args):
        if isinstance(args, type(self)):
            args = args.data
        return self.data.__mod__(args)

    def __rmod__(self, template):
        return str(template) % self.data

    def __mul__(self, n):
        return self.data * n

    def __ne__(self, other):
        if isinstance(other, type(self)):
            other = other.data
        return self.data != other

    #def __reduce__(self):
    #    raise TypeError('cannot pickle {0} object'.format(type(self).__name__))

    @property
    def data(self):
        if self.result is not None:
            return self.result

        result = []

        for unit in self.units:
            result.append(unit.base)
            if unit.appendix is not None:
                substring = 'x = {0}'.format(unit.appendix)
                namespace = self.local_globals.copy()
                namespace.update(self.local_nonlocals)
                namespace.update(self.local_locals)
                try:
                    exec(substring, namespace)
                except SyntaxError as e:
                    raise SyntaxError('lazy f-string: invalid syntax') from e
                result.append(str(namespace['x']))

        self.result = ''.join(result)
        del self.units
        del self.local_locals

        return self.result


class ProxyModule(sys.modules[__name__].__class__):
    old_str = str

    def __call__(self, string, lazy=True):
        if not lazy:
            raise NotImplementedError('Only lazy mode is allowed.')

        return LazyString(
            [ChainUnit(base=x[0], appendix=x[1], lazy=lazy) for x in Formatter().parse(string)],
            {**inspect.stack(0)[1].frame.f_locals},
            {**inspect.stack(0)[1].frame.f_globals},
            self.sum_of_nonlocals(inspect.stack(0)[1].frame.f_back, self.get_qualname(inspect.stack(0)[1].frame.f_code)),
            lazy,
        )

    def sum_of_nonlocals(self, first_frame, base_qualname):
        if first_frame is None:
            return {}

        all_locals = []
        while first_frame is not None:
            code = first_frame.f_code

            qualname = self.get_qualname(code)
            if qualname is not None:
                if self.startswith(base_qualname.split('.'), qualname.split('.')):
                    all_locals.append(first_frame.f_locals)

            first_frame = first_frame.f_back

        result = {}
        index = len(all_locals) - 1

        while index >= 0:
            result.update(all_locals[index])
            index -= 1

        return result

    @staticmethod
    def get_qualname(code):
        functions = []

        for function in gc.get_referrers(code):
            if getattr(function, '__code__', None) is code:
                if callable(function):
                    functions.append(function)

        if functions:
            function = functions[0]
            return function.__qualname__

    @staticmethod
    def startswith(iterable, second_iterable):
        if len(iterable) < len(second_iterable):
            return False

        for element, second_element in zip(second_iterable, iterable):
            if element != second_element:
                return False

        return True

    def __str__(self):
        return 'f'

    def __repr__(self):
        return 'f'


sys.modules[__name__].__class__ = ProxyModule
