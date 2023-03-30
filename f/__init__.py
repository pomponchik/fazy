import sys
import inspect
from string import Formatter


class ChainUnit:
    def __init__(self, base, appendix=None, lazy=True):
        self.base = base
        self.appendix = appendix
        if self.appendix is not None:
            if self.appendix == '':
                raise SyntaxError('lazy f-string: empty expression not allowed')

class LazyString:
    def __init__(self, units, local_locals, lazy):
        self.units = units
        self.local_locals = local_locals
        self.lazy = lazy
        self.result = None

    def get(self):
        if self.result is not None:
            return self.result

        result = []

        for unit in self.units:
            result.append(unit.base)
            if unit.appendix is not None:
                substring = f'x = {unit.appendix}'
                namespace = {**self.local_locals}
                try:
                    exec(substring, namespace)
                except SyntaxError as e:
                    raise SyntaxError('lazy f-string: invalid syntax') from e
                result.append(str(namespace['x']))

        self.result = ''.join(result)
        del self.units
        del self.local_locals

        return self.result

    def __str__(self):
        return self.get()

    def __getattribute__(self, name):
        try:
            result = object.__getattribute__(self, name)
            print(1, name, result)

        except AttributeError:
            result = getattr(self.get(), name)
            print(2, name, result)

        return result



class ProxyModule(sys.modules[__name__].__class__):
    def __call__(self, string, lazy=True):
        if not lazy:
            raise NotImplementedError('Only lazy mode is allowed.')

        return LazyString(
            [ChainUnit(base=x[0], appendix=x[1], lazy=lazy) for x in Formatter().parse(string)],
            {**inspect.stack(0)[1].frame.f_locals},
            lazy,
        )

sys.modules[__name__].__class__ = ProxyModule
