from collections import UserString


class LazyString(UserString, str):
    __slots__ = ('units', 'local_locals', 'local_globals', 'local_nonlocals', 'lazy', 'result')

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

    def __rmul__(self, n):
        return self.data * n

    def __ne__(self, other):
        if isinstance(other, type(self)):
            other = other.data
        return self.data != other

    def __reduce__(self):
        raise TypeError('cannot pickle {0} object'.format(type(self).__name__))

    def __setattr__(self, name, value):
        if name not in type(self).__slots__:
            raise AttributeError(
                "'{0}' object has no attribute '{1}'".format(type(self).__name__, name)
            )
        object.__setattr__(self, name, value)

    def replace(self, old, new, maxsplit=-1):
        if isinstance(old, type(self)):
            old = old.data
        if isinstance(new, type(self)):
            new = new.data
        return self.data.replace(old, new, maxsplit)

    def split(self, sep=None, maxsplit=-1):
        if isinstance(sep, type(self)):
            sep = sep.data
        return self.data.split(sep, maxsplit)

    def rsplit(self, sep=None, maxsplit=-1):
        if isinstance(sep, type(self)):
            sep = sep.data
        return self.data.rsplit(sep, maxsplit)

    def lower(self):
        return self.data.lower()

    def upper(self):
        return self.data.upper()

    def zfill(self, width):
        return self.data.zfill(width)

    def translate(self, *args):
        return self.data.translate(*args)

    def title(self):
        return self.data.title()

    def startswith(self, prefix, *other_args):
        if isinstance(prefix, type(self)):
            prefix = prefix.data
        return self.data.startswith(prefix, *other_args)

    def endswith(self, suffix, *other_args):
        if isinstance(suffix, type(self)):
            suffix = suffix.data
        return self.data.endswith(suffix, *other_args)

    def index(self, sub, *other):
        if isinstance(sub, type(self)):
            sub = sub.data
        return self.data.index(sub, *other)

    def rindex(self, sub, *other):
        if isinstance(sub, type(self)):
            sub = sub.data
        return self.data.rindex(sub, *other)

    def center(self, width, *others):
        others = [other.data if isinstance(other, type(self)) else other for other in others]
        return self.data.center(width, *others)

    def join(self, iterable):
        iterable = [item.data if isinstance(item, type(self)) else item for item in iterable]
        return self.data.join(iterable)

    def capitalize(self):
        return self.data.capitalize()

    def encode(self, **kwargs):
        return self.data.encode(**kwargs)

    def casefold(self):
        return self.data.casefold()

    def expandtabs(self, tabsize=8):
        return self.data.expandtabs(tabsize)

    def removeprefix(self, prefix):
        if isinstance(prefix, type(self)):
            prefix = prefix.data
        return self.data.removeprefix(prefix)

    def removesuffix(self, suffix):
        if isinstance(suffix, type(self)):
            suffix = suffix.data
        return self.data.removesuffix(suffix)

    def lstrip(self, chars=None):
        if isinstance(chars, type(self)):
            chars = chars.data
        return self.data.lstrip(chars)

    def rstrip(self, chars=None):
        if isinstance(chars, type(self)):
            chars = chars.data
        return self.data.rstrip(chars)

    def ljust(self, width, *args):
        args = [item.data if isinstance(item, type(self)) else item for item in args]
        return self.data.ljust(width, *args)

    def rjust(self, width, *args):
        args = [item.data if isinstance(item, type(self)) else item for item in args]
        return self.data.rjust(width, *args)

    def encode(self, **kwargs):
        kwargs = {key: value.data if isinstance(value, type(self)) else value for key, value in kwargs.items()}
        return self.data.encode(**kwargs)

    @staticmethod
    def maketrans(x, *others):
        others = [item.data if isinstance(item, UserString) else item for item in others]
        x = x.data if isinstance(x, UserString) else x

        if isinstance(x, str):
            return str.maketrans(x, *others)

        first_item = {}
        for key, value in x.items():
            key = key.data if isinstance(key, UserString) else key
            value = value.data if isinstance(value, UserString) else value
            first_item[key] = value

        return str.maketrans(first_item, *others)

    def partition(self, sep):
        sep = sep.data if isinstance(sep, type(self)) else sep
        return self.data.partition(sep)

    def rpartition(self, sep):
        sep = sep.data if isinstance(sep, type(self)) else sep
        return self.data.rpartition(sep)

    def swapcase(self):
        return self.data.swapcase()

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
        del self.local_nonlocals
        del self.local_globals

        return self.result
