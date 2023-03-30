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

def proxy_dunders(Class):
    all_names = [
        '__add__',
        '__contains__',
        '__format__',
        '__ge__',
        '__getnewargs__',
        '__gt__',
        '__hash__',
        '__iter__',
        '__le__',
        '__len__',
        '__lt__',
        '__mul__',
        '__mod__',
        '__ne__',
        '__reduce__',
        '__reduce_ex__',
        '__repr__',
        '__rmod__',
        '__rmul__',
        '__str__',
        '__eq__',
    ]
    #for name in dir(''):
    #    if not name.startswith('__'):
    #        if name not in ('zfill', 'upper'):
    #            all_names.append(name)


    for name in all_names:
        try:
            @wraps(getattr(Class, name))
            def wrapper(*args, **kwargs):
                string = args[0].get()
                string_attribute = getattr(string, name)
                result = string_attribute(*(args[1:]), **kwargs)
                return result
            setattr(Class, name, wrapper)
        except AttributeError:
            @wraps(getattr(str, name))
            def wrapper(*args, **kwargs):
                string = args[0].get()
                string_attribute = getattr(string, name)
                result = string_attribute(*(args[1:]), **kwargs)

                return result
            setattr(Class, name, wrapper)
    return Class

@proxy_dunders
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
                substring = 'x = {0}'.format(unit.appendix)
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
