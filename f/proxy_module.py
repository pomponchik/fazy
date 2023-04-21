import gc
import sys
import inspect
from string import Formatter

from f.chain_unit import ChainUnit
from f.lazy_string import LazyString


class ProxyModule(sys.modules[__name__].__class__):
    old_str = str

    def __call__(self, string, lazy=True):
        if not lazy:
            raise NotImplementedError('Only lazy mode is allowed.')

        if isinstance(string, LazyString):
            string = string.data

        return LazyString(
            [ChainUnit(base=x[0], appendix=x[1], lazy=lazy) for x in Formatter().parse(string)],
            {**inspect.stack(0)[1].frame.f_locals},
            {**inspect.stack(0)[1].frame.f_globals},
            self.sum_of_nonlocals(inspect.stack(0)[1].frame.f_back, self.get_qualname(inspect.stack(0)[1].frame.f_code)),
            lazy,
        )

    def sum_of_nonlocals(self, first_frame, base_qualname):
        if first_frame is None or base_qualname is None:
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
            if inspect.isgenerator(function):
                if getattr(function, 'gi_code', None) is code:
                    functions.append(function)
            elif callable(function):
                if getattr(function, '__code__', None) is code:
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
