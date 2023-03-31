import sys
import inspect
from string import Formatter
from functools import wraps


class ChainUnit:
    def __init__(self, base, appendix=None, lazy=True):
        self.base = base
        self.appendix = appendix
        if self.appendix is not None:
            if self.appendix == '':
                raise SyntaxError('lazy f-string: empty expression not allowed')


class LazyString:
    def __init__(self, units, local_locals, local_globals, lazy):
        self.units = units
        self.local_locals = local_locals
        self.local_globals = local_globals
        self.lazy = lazy
        self.result = None

    def __str__(self):
        return str(self.get())

    def __repr__(self):
        return repr(self.get())

    def __eq__(self, other):
        return self.get().__eq__(other)

    def __add__(self, other):
        if isinstance(other, type(self)):
            other = other.get()
        return self.get().__add__(other)

    def __radd__(self, other):
        if isinstance(other, type(self)):
            other = other.get()
        if not isinstance(other, str):
            raise TypeError('can only concatenate str (not "{0}") to str'.format(type(other).__name__))

        return other + self.get()

    def get(self):
        if self.result is not None:
            return self.result

        result = []

        for unit in self.units:
            result.append(unit.base)
            if unit.appendix is not None:
                substring = 'x = {0}'.format(unit.appendix)
                namespace = self.local_globals.copy()
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
            lazy,
        )

    def __str__(self):
        return 'f'

sys.modules[__name__].__class__ = ProxyModule
