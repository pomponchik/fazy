![logo](https://raw.githubusercontent.com/pomponchik/fazy/develop/docs/assets/logo_3.png)

[![Downloads](https://static.pepy.tech/badge/fazy/month)](https://pepy.tech/project/fazy)
[![Downloads](https://static.pepy.tech/badge/fazy)](https://pepy.tech/project/fazy)
[![codecov](https://codecov.io/gh/pomponchik/fazy/branch/main/graph/badge.svg)](https://codecov.io/gh/pomponchik/fazy)
[![Test-Package](https://github.com/pomponchik/fazy/actions/workflows/coverage.yml/badge.svg)](https://github.com/pomponchik/fazy/actions/workflows/coverage.yml)
[![PyPI version](https://badge.fury.io/py/fazy.svg)](https://badge.fury.io/py/fazy)
[![Python versions](https://img.shields.io/pypi/pyversions/fazy.svg)](https://pypi.python.org/pypi/fazy)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


Lazy f-strings are the holy grail of Python development. Now it is found.


## Table of contents

- [**Quick start**](#quick-start)
- [**Additional features**](#additional-features)
- [**The problem**](#the-problem)
- [**How does it work?**](#how-does-it-work)
- [**Limitations**](#limitations)
- [**Benchmark**](#benchmark)


## Quick start

Install it:

```bash
pip install fazy
```

And use:

```python
>>> import f
>>>
>>> number = 33
>>> f('{number} kittens drink milk')
'33 kittens drink milk'
```

## Additional features

You can execute the string not in lazy mode:

```python
>>> f('{number} kittens drink milk', lazy=False)
'33 kittens drink milk'
```

By default, you cannot use variables as templates. When you try to do this, you will see an `SyntaxError` (the example will not work in REPL and in the global scope, that's why you don't see `>>>`):

```python
def function():
    number = 33
    template = '{number} kittens drink milk'
    print(f(template))

function()
# SyntaxError: Unsafe use of a variable as a template.
```

However, you can disable this check:

```python
template = '{number} kittens drink milk'
f(template, safe=False)
```

All scopes of variable names are available to you, including variables declared in closures. If you disable data extraction from closures, you can greatly speed up the execution of the function:

```python
>>> f('{number} kittens drink milk', closures=False)
'33 kittens drink milk'
```


## The problem

The main problem that this library solves is the transfer of the cost of calculating the extrapolation of a string from the moment when it is determined to the moment when it is used. And all this while preserving the classic look of the f-string, which we are so used to on modern versions of Python.

The main use case that the author had in mind is related to logging. The fact is that many messages that are created for logging may eventually not be printed, because the logging level is too low for them. The classic solution to the problem is to calculate the string in a [lazy](https://en.wikipedia.org/wiki/Lazy_evaluation) way. However, until now, this solution has been incompatible with the convenient syntax of f-strings. You needed to use % expressions for this, it looks much worse.

The new way of writing logs is not very different from the old one. Try to execute this piece of code:

```python
import logging
import f


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)

number = 33
logging.info(f('{number} kittens drink milk'))
```

You will see a message similar to this:

```
2023-04-18 15:15:43,200 [INFO] 33 kittens drink milk
```

However, if you replace `level=logging.INFO` on `level=logging.ERROR`, you won't see anything in the console. If you were using classical f-strings here, the extrapolation would happen anyway. However, using this library in the second case, the string will not be calculated.

To feel the advantages of this approach, let's try to display an object whose string representation is calculated for a very long time:

```python
from time import sleep
import logging
import f


class LongPrintable:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        sleep(10.0)
        return str(self.data)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)

number = LongPrintable(33)
logging.debug(f('{number} kittens drink milk'))
```

This code will be executed almost instantly! However, you will immediately notice the expected delay if you replace `logging.debug` with `logging.info`.

A side effect of this library is the fact that it allows you to use syntax close to f-strings on Python versions lower than 3.6. However, this feature was not the main one during development and was not tested separately. If you are using fairly old versions of Python - try it, most likely everything will work. If you are only interested in supporting f-syntax on older versions of Python without lazy calculations, you may be interested in another similar library.


## How does it work?

The function `f` returns an object of the `LazyString` class. This class is inherited from `str` and wraps almost all the functionality inherent in ordinary strings. References to variables from multiple scopes are stored inside the returned object. At the first attempt to use the object, the final row is calculated inside it and then the object behaves like it. At the same time, references to variables from all scopes are destroyed and the final row is returned from the cache during subsequent calls.

There are 3 scopes of variable names that are extracted from the call stack to allow them to be used inside expressions:

1. **Local variables**.
2. **Global variables**.
3. **Intermediate variables** that are used, for example, when creating [closures](https://en.wikipedia.org/wiki/Closure_(computer_programming)). To give them a more precise definition, these are such local variables of all functions higher up the call stack, which refer to functions that in the code wrap the function being executed at the moment (I know this sentence may not be so easy to read and understand the first time). This means that, going through the call stack, we ignore all scopes with local variables for functions that are not the parents of the function being executed at the moment.

As you might guess from the size of the description, the most interesting type of scopes is the third - intermediate variables. The expected approach to determine the nesting of functions is an analysis of the source code. However, compiling a large amount of source code just to figure out which function wraps another one would be too costly. Therefore, in this case, a hack is used based on knowledge of how memory management occurs inside the interpreter. The fact is that the garbage collector knows about all the objects that exist in memory, as well as about the links between them. The function in which a particular frame of the call stack is executed can be found by requesting from the gc all objects containing references to it. After retrieving the function object, you can determine whether it is the parent of the currently executed one. To do this, you just need to compare their full names (qualnames) stored in the metadata of the functions.

Another couple of words deserves a description of protection from a call with a template in the form of a variable. As you could already understand from the description above, by default you can call the function `f` only with a string literal as an argument. This is necessary to protect the string from attacks that allow arbitrary code to be executed. Checking whether a string is a literal and not a variable is performed by analyzing an abstract syntax tree (AST). Through the stack, we find the function in which the code is currently running. Next, we analyze this code in search of situations where the function `f` is called without a literal as an argument. If such a situation occurs at least 1 time in the line in which the code is currently being executed, we raise `SyntaxError`. However, it should be borne in mind that this protection cannot work in REPL, because there are difficulties in extracting the source code of the function for AST analysis. There were also problems with how to extract data about the module in which the code is executed, so the protection will not work in the global scope either. And finally, this check does not work on Python 3.7.


## Limitations

Based on the description of the internal structure of the library, you can understand that there are some limitations that should be taken into account. Here are some of them:

- **The performance is obviously less** than that of the original f-strings embedded in the interpreter. Read more about this in the section with [benchmark](#benchmark).
- **Mutable objects can change their state between the time the references to them are saved and the final calculation of the string**. This means, for example, that if you create a `LazyString` object containing a reference to the list, then add another element to the list, and after that calculate the string - you will see the list in the already changed state in this line.
- Heavy objects may not be destroyed during garbage collection as long as references to them are stored inside the `LazyString`. This may look like a memory leak in some rare cases and you should keep this in mind.
- **`LazyString` objects, despite their almost complete similarity to `str`, still do not fully replace ordinary strings**. For example, such a string cannot be written to a file or serialized using pickle. Many built-in Python functions expect only ordinary strings and it is impossible to fake it in any way. There is no way to get the full functionality of regular strings from `LazyString`, except to convert `LazyString` to `str`, like this:

  ```python
  str(f('some string'))
  ```

- **Some methods of the `str` class also necessarily expect `str` objects as an argument**. These are methods such as [count](https://docs.python.org/3/library/stdtypes.html#str.count), [replace](https://docs.python.org/3/library/stdtypes.html#str.replace), [center](https://docs.python.org/3/library/stdtypes.html#str.center), [join](https://docs.python.org/3/library/stdtypes.html#str.join), [encode](https://docs.python.org/3/library/stdtypes.html#str.encode), [maketrans](https://docs.python.org/3/library/stdtypes.html#str.maketrans), [split](https://docs.python.org/3/library/stdtypes.html#str.split) and [rsplit](https://docs.python.org/3/library/stdtypes.html#str.rsplit), [index](https://docs.python.org/3/library/stdtypes.html#str.index) and [rindex](https://docs.python.org/3/library/stdtypes.html#str.rindex), [removeprefix](https://docs.python.org/3/library/stdtypes.html#str.removeprefix) and [removesuffix](https://docs.python.org/3/library/stdtypes.html#str.removesuffix), [find](https://docs.python.org/3/library/stdtypes.html#str.find) and [rfind](https://docs.python.org/3/library/stdtypes.html#str.rfind), [startswith](https://docs.python.org/3/library/stdtypes.html#str.startswith) and [endswith](https://docs.python.org/3/library/stdtypes.html#str.endswith), [ljust](https://docs.python.org/3/library/stdtypes.html#str.ljust) and [rjust](https://docs.python.org/3/library/stdtypes.html#str.rjust), [strip](https://docs.python.org/3/library/stdtypes.html#str.strip), [lstrip](https://docs.python.org/3/library/stdtypes.html#str.lstrip) and [rstrip](https://docs.python.org/3/library/stdtypes.html#str.rstrip), [partition](https://docs.python.org/3/library/stdtypes.html#str.partition) and [rpartition](https://docs.python.org/3/library/stdtypes.html#str.rpartition). This behavior cannot be changed, so when using lazy strings, it is most reliable to immediately convert them to regular ones. In addition, expressions using the `in` operator like this one will not work correctly:

  ```python
  f('some string') in 'some another string'
  ```
- A special **f-string [formatting language](https://docs.python.org/3/reference/lexical_analysis.html#f-strings) is not supported**. All that is available is the usual embedding of expressions right inside the string.
- In most code editors and IDE, special **syntax highlighting for f-strings will not work**.


## Benchmark

If you have read the text above, you already know that this implementation is slower than the original f-strings. But for how long?

In fact, it is impossible to accurately predict the complexity of operations related to string extrapolation. It depends on many factors, including the depth of the call stack, the number of local and global variables, whether this function is nested in other functions, and also, obviously, the complexity of executing the expression that you have embedded in the string.

For example, we will consider the degenerate case:

```python
from time import perf_counter
import f


t1 = perf_counter()

for number in range(10000):
    str(f('the number is {number}'))

print(perf_counter() - t1)
```

On my computer (a MacBook Pro with an Apple M1 Pro processor), the execution of this code takes about 2 seconds, that is, about **0.0002 seconds for 1 iteration**. However, if I replace `str(f('the number is {number}'))` with `str(f'the number is {number}')`, the execution time will be 0.0022 seconds, about **0.00000022 seconds for 1 iteration**.

> So, the original f-strings in this case turned out to be about **1000 times faster**.

However, this does not mean that f-strings are faster in all cases. In real use, you should consider how fast the expressions that you insert into the f-strings are evaluated. If this is significantly slower than actually required for extrapolation, saving on deferred extrapolation may make sense.

Most of the extrapolation time is actually taken not by the extrapolation itself, but by collecting various data for display from the stack and the garbage collector. Unfortunately, if you want to completely replicate the behavior of the original f-strings, these costs are unavoidable.
