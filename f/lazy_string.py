from collections import UserString
from typing import Union, List, Dict, Tuple, Iterable, Callable, Optional, Any

from f.chain_unit import ChainUnit


class LazyString(UserString, str):  # type: ignore[misc]
    __slots__ = ('units', 'local_locals', 'local_globals', 'local_nonlocals', 'lazy', 'result')

    def __init__(self, units: List[ChainUnit], local_locals: Dict[str, Any], local_globals: Dict[str, Any], local_nonlocals: Dict[str, Any], lazy: bool) -> None:
        self.units: List[ChainUnit] = units
        self.local_locals: Dict[str, Any] = local_locals
        self.local_globals: Dict[str, Any] = local_globals
        self.local_nonlocals: Dict[str, Any] = local_nonlocals
        self.lazy: bool = lazy
        self.result: Optional[str] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> 'LazyString':
        return str.__new__(cls)

    def __add__(self, other: Union['LazyString', str]) -> str:
        if isinstance(other, type(self)):
            other = other.data
        return self.data.__add__(other)

    def __radd__(self, other: Union['LazyString', str]) -> str:
        return other + self.data

    def __getitem__(self, index: int) -> str:
        return self.data.__getitem__(index)

    def __getnewargs__(self) -> Tuple[List[ChainUnit], Dict[str, Any], Dict[str, Any], Dict[str, Any], bool]:
        return (self.units, self.local_locals, self.local_globals, self.local_nonlocals, self.lazy)

    def __mod__(self, args) -> str:
        if isinstance(args, type(self)):
            args = args.data
        return self.data.__mod__(args)

    def __rmod__(self, template: Union['LazyString', str]) -> str:
        return str(template) % self.data

    def __mul__(self, n: int) -> str:
        return self.data * n

    def __rmul__(self, n: int) -> str:
        return self.data * n

    def __ne__(self, other: Union['LazyString', str]) -> bool:
        if isinstance(other, type(self)):
            other = other.data
        return self.data != other

    def __reduce__(self) -> Union[str, Tuple[Callable[[], Any], Tuple[Any, ...], Iterable[Any], Iterable[Any], Iterable[Any]]]:
        raise TypeError('cannot pickle {0} object'.format(type(self).__name__))

    def __setattr__(self, name: str, value: Any) -> None:
        if name not in type(self).__slots__:
            raise AttributeError(
                "'{0}' object has no attribute '{1}'".format(type(self).__name__, name)
            )
        object.__setattr__(self, name, value)

    def replace(self, old: Union['LazyString', str], new: Union['LazyString', str], maxsplit: int =-1) -> str:
        if isinstance(old, type(self)):
            old = old.data
        if isinstance(new, type(self)):
            new = new.data
        return self.data.replace(old, new, maxsplit)

    def split(self, sep: Optional[Union['LazyString', str]] = None, maxsplit: int = -1) -> List[str]:
        if isinstance(sep, type(self)):
            sep = sep.data
        return self.data.split(sep, maxsplit)

    def rsplit(self, sep: Optional[Union['LazyString', str]] = None, maxsplit: int = -1) -> List[str]:
        if isinstance(sep, type(self)):
            sep = sep.data
        return self.data.rsplit(sep, maxsplit)

    def lower(self) -> str:
        return self.data.lower()

    def upper(self) -> str:
        return self.data.upper()

    def zfill(self, width: int) -> str:
        return self.data.zfill(width)

    def translate(self, table: Dict[int, int]) -> str:
        return self.data.translate(table)

    def title(self) -> str:
        return self.data.title()

    def startswith(self, prefix: Union['LazyString', str], *other_args: Union['LazyString', str]) -> bool:
        if isinstance(prefix, type(self)):
            prefix = prefix.data
        converted_other_args = [x if not isinstance(x, type(self)) else x.data for x in other_args]
        return self.data.startswith(prefix, *converted_other_args)

    def endswith(self, suffix: Union['LazyString', str, Tuple[Union['LazyString', str], ...]], *other_args: int) -> bool:
        if isinstance(suffix, type(self)):
            suffix = suffix.data
        elif isinstance(suffix, tuple):
            suffix = tuple(*(x.data if isinstance(x, type(self)) else x for x in suffix))
        return self.data.endswith(suffix, *other_args)

    def index(self, sub: Union['LazyString', str], *other: int) -> int:
        if isinstance(sub, type(self)):
            sub = sub.data
        return self.data.index(sub, *other)

    def rindex(self, sub: Union['LazyString', str], *other: int) -> int:
        if isinstance(sub, type(self)):
            sub = sub.data
        return self.data.rindex(sub, *other)

    def center(self, width: int, *others: Union['LazyString', str]) -> str:
        converted_others = [other.data if isinstance(other, type(self)) else other for other in others]
        return self.data.center(width, *converted_others)

    def join(self, iterable: Iterable[Union['LazyString', str]]) -> str:
        converted_iterable = [item.data if isinstance(item, type(self)) else item for item in iterable]
        return self.data.join(converted_iterable)

    def capitalize(self) -> str:
        return self.data.capitalize()

    def casefold(self) -> str:
        return self.data.casefold()

    def expandtabs(self, tabsize: int = 8) -> str:
        return self.data.expandtabs(tabsize)

    def removeprefix(self, prefix: Union['LazyString', str]) -> str:
        if isinstance(prefix, type(self)):
            prefix = prefix.data
        return self.data.removeprefix(prefix)  # type: ignore[attr-defined, no-any-return]

    def removesuffix(self, suffix: Union['LazyString', str]) -> str:
        if isinstance(suffix, type(self)):
            suffix = suffix.data
        return self.data.removesuffix(suffix)  # type: ignore[attr-defined, no-any-return]

    def lstrip(self, chars: Optional[Union['LazyString', str]] = None) -> str:
        if isinstance(chars, type(self)):
            chars = chars.data
        return self.data.lstrip(chars)

    def rstrip(self, chars: Optional[Union['LazyString', str]] = None) -> str:
        if isinstance(chars, type(self)):
            chars = chars.data
        return self.data.rstrip(chars)

    def ljust(self, width, *args):
        args = [item.data if isinstance(item, type(self)) else item for item in args]
        return self.data.ljust(width, *args)

    def rjust(self, width, *args):
        args = [item.data if isinstance(item, type(self)) else item for item in args]
        return self.data.rjust(width, *args)

    def encode(self, **kwargs: Union['LazyString', str]) -> bytes:
        kwargs = {key: value.data if isinstance(value, type(self)) else value for key, value in kwargs.items()}
        return self.data.encode(**kwargs)

    @staticmethod
    def maketrans(x: Union[Dict[Union[int, str, UserString], Optional[Union[int, str, UserString]]], str, UserString], *others: Union[str, UserString]) -> Dict[int, int]:
        converted_others = [item.data if isinstance(item, UserString) else item for item in others]
        x = x.data if isinstance(x, UserString) else x

        if isinstance(x, str):
            return str.maketrans(x, *converted_others)

        first_item = {}
        for key, value in x.items():
            key = key.data if isinstance(key, UserString) else key
            value = value.data if isinstance(value, UserString) else value
            first_item[key] = value

        return str.maketrans(first_item, *converted_others)

    def partition(self, sep: Union['LazyString', str]) -> Tuple[str, str, str]:
        sep = sep.data if isinstance(sep, type(self)) else sep
        return self.data.partition(sep)

    def rpartition(self, sep: Union['LazyString', str]) -> Tuple[str, str, str]:
        sep = sep.data if isinstance(sep, type(self)) else sep
        return self.data.rpartition(sep)

    def swapcase(self) -> str:
        return self.data.swapcase()

    @property
    def data(self) -> str:
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
