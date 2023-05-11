import gc
import sys
import ast
import inspect
from string import Formatter

from f.chain_unit import ChainUnit
from f.lazy_string import LazyString


class ProxyModule(sys.modules[__name__].__class__):
    old_str = str

    def __call__(self, string, lazy=True, safe=True, closures=True):
        if isinstance(string, LazyString):
            return string

        base_frame = inspect.stack(0)[1].frame

        result = LazyString(
            [ChainUnit(base=x[0], appendix=x[1], lazy=lazy) for x in Formatter().parse(string)],
            {**base_frame.f_locals},
            {**base_frame.f_globals},
            self.sum_of_nonlocals(
                base_frame.f_back,
                self.get_qualname(base_frame.f_code, raise_if_not_literal=safe, code_line=base_frame.f_lineno),
                closures,
                safe,
            ),
            lazy,
        )

        if lazy:
            return result
        return result.data

    def sum_of_nonlocals(self, first_frame, base_qualname, closures, safe):
        if not closures or first_frame is None or base_qualname is None:
            return {}

        all_locals = []
        while first_frame is not None:
            code = first_frame.f_code

            qualname = self.get_qualname(code, raise_if_not_literal=False, code_line=0)
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

    @classmethod
    def get_qualname(cls, code, raise_if_not_literal, code_line):
        functions = []

        for function in gc.get_referrers(code):
            maybe_code = None
            if inspect.isgenerator(function):
                maybe_code = getattr(function, 'gi_code', None)
            elif callable(function):
                maybe_code = getattr(function, '__code__', None)
            if maybe_code is not None:
                functions.append(function)

        if functions:
            function = functions[0]
            if raise_if_not_literal:
                cls.check_code(function, code, code_line)
            return function.__qualname__

    @staticmethod
    def check_code(function, code, code_line):
        try:
            if inspect.isgenerator(function):
                code_strings, begin_code_line_number = inspect.getsourcelines(code)
            else:
                code_strings, begin_code_line_number = inspect.getsourcelines(function)
        except:
            return

        spaces_count = 0
        for letter in code_strings[0]:
            if not letter.isspace():
                break
            spaces_count += 1

        code_strings = [x[spaces_count:] for x in code_strings]

        full_code = ''.join(code_strings)
        ast_of_code = ast.parse(full_code)
        expected_line_number = begin_code_line_number

        flag = True
        class ConstantVisitor(ast.NodeVisitor):
            def visit_Call(self, node):
                nonlocal flag
                if node.lineno + begin_code_line_number - 1 == code_line:
                    if hasattr(node.func, 'id') and node.func.id == 'f':
                        if len(node.args) == 1 and isinstance(node.args[0], ast.Constant):
                            flag *= True
                        elif len(node.args) == 1 and isinstance(node.args[0], ast.Call) and hasattr(node.args[0].func, 'id') and node.args[0].func.id == 'f':
                            flag *= True
                            for arg in node.args:
                                ConstantVisitor().visit(arg)
                            for keyword in node.keywords:
                                ConstantVisitor().visit(keyword.value)
                        else:
                            flag *= False
                    elif isinstance(node.func, ast.Attribute):
                        ConstantVisitor().visit(node.func.value)
                        for arg in node.args:
                            ConstantVisitor().visit(arg)
                        for keyword in node.keywords:
                            ConstantVisitor().visit(keyword.value)
                    else:
                        for arg in node.args:
                            ConstantVisitor().visit(arg)
                        for keyword in node.keywords:
                            ConstantVisitor().visit(keyword.value)

        ConstantVisitor().visit(ast_of_code)

        if not flag and not (sys.version_info < (3, 8)):
            raise SyntaxError('Unsafe use of a variable as a template.')


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
