import inspect
import sys
import gc


def function():
    print(dir(inspect.stack(0)[0].frame.f_code))
    print('co_qualname' in dir(inspect.stack(0)[0].frame.f_code))
    print(inspect.getmembers(inspect.stack(0)[0].frame))
    print()
    print()
    print()
    print(inspect.stack(0))
    print(dir(sys._getframe(0).f_code))
    print('co_qualname' in dir(sys._getframe(0).f_code))
    print()
    print()
    print()
    print(inspect.stack(0)[0].frame.f_code.co_cellvars)

l = [function]

function()
