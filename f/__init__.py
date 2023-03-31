import sys
import inspect
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
    def __call__(self, string, lazy=True):
        if not lazy:
            raise NotImplementedError('Only lazy mode is allowed.')

        return LazyString(
            [ChainUnit(base=x[0], appendix=x[1], lazy=lazy) for x in Formatter().parse(string)],
            {**inspect.stack(0)[1].frame.f_locals},
            {**inspect.stack(0)[1].frame.f_globals},
            self.sum_of_nonlocals(inspect.stack(0)[1].frame.f_back),
            lazy,
        )

    def sum_of_nonlocals(self, first_frame):
        #print(inspect.getframeinfo(first_frame))
        if first_frame is None:
            return {}

        all_locals = []
        while first_frame is not None:
            #code = first_frame.f_code
            #print(dir(code))
            all_locals.append(first_frame.f_locals)
            first_frame = first_frame.f_back

        result = {}
        index = len(all_locals) - 1

        #all_locals.reverse()
        while index >= 0:
            result.update(all_locals[index])
            index -= 1

        return result

    def __str__(self):
        return 'f'

    def __repr__(self):
        return 'f'

sys.modules[__name__].__class__ = ProxyModule
