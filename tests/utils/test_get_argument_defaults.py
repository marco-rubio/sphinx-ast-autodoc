"""Tests for the `utils.get_argument_defaults` function"""
import ast
import inspect

import pytest

from sphinx_ast_autodoc.utils import get_argument_defaults

EMPTY_VALUE = inspect.Parameter.empty


@pytest.mark.parametrize(
    "code,expected_defaults",
    [
        ["""def fun(a): pass""", [EMPTY_VALUE]],
        ["""def fun(a=1): pass""", [1]],
        ["""def fun(a, b=1): pass""", [EMPTY_VALUE, 1]],
        ["""def fun(a, b, c=2): pass""", [EMPTY_VALUE, EMPTY_VALUE, 2]],
        ["""def fun(a, b=1, c=2): pass""", [EMPTY_VALUE, 1, 2]],
        ["""def func(*args, b=1): pass""", [EMPTY_VALUE, 1]],
        ["""def func(*args, b=1, **ops): pass""", [EMPTY_VALUE, 1, EMPTY_VALUE]],
        ["""def fun(a, b=1, /): pass""", [EMPTY_VALUE, 1]],
        ["""def fun(a, b, /, c=1): pass""", [EMPTY_VALUE, EMPTY_VALUE, 1]],
        ["""def fun(a, b=1, /, c=2): pass""", [EMPTY_VALUE, 1, 2]],
        ["""def fun(a, b=1, /, c=2, *, d=3): pass""", [EMPTY_VALUE, 1, 2, 3]],
        [
            """def fun(a, b=1, /, c=2, *args, d=3): pass""",
            [EMPTY_VALUE, 1, 2, EMPTY_VALUE, 3],
        ],
    ],
)
def test_it_processes_argument_defaults_correctly(code, expected_defaults):
    """Tests that it processes argument defaults correctly"""

    function_def = ast.parse(code).body[0]
    defaults = list(get_argument_defaults(function_def.args))

    assert defaults == expected_defaults
