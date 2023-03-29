import inspect
from string import Formatter
from dataclasses import dataclass

@dataclass
class ChainUnit:
    base: str
    appendix: str = None


class LazyString:
    def __init__(self, units, local_locals):
        self.units = units
        self.local_locals = local_locals
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
                exec(substring, namespace)
                result.append(str(namespace['x']))

        self.result = ''.join(result)
        del self.units
        del self.local_locals

        return self.result

    def __str__(self):
        return self.get()

def f(string):
    return LazyString(
        [ChainUnit(base=x[0], appendix=x[1]) for x in Formatter().parse(string)],
        {**inspect.stack(0)[1].frame.f_locals},
    )
