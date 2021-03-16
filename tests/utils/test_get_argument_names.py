"""Tests for the `utils.get_argument_names` function"""
import ast

import pytest

from sphinx_ast_autodoc.utils import get_argument_names


@pytest.mark.parametrize(
    "code,expected_names",
    [
        ["""def fun(a): pass""", ["a"]],
        ["""def fun(a, b): pass""", ["a", "b"]],
        ["""def fun(a, b, /): pass""", ["a", "b"]],
        ["""def fun(a, b, /, c): pass""", ["a", "b", "c"]],
        ["""def fun(a, b, *args): pass""", ["a", "b", "args"]],
        ["""def fun(a, b, *, c): pass""", ["a", "b", "c"]],
        ["""def fun(a, b, /, c, *, d): pass""", ["a", "b", "c", "d"]],
        ["""def fun(a, b, /, c, *, d, **ops): pass""", ["a", "b", "c", "d", "ops"]],
    ],
)
def test_it_processes_argument_names_correctly(code, expected_names):
    """Tests that it processes argument names correctly"""

    function_def = ast.parse(code).body[0]
    params = list(get_argument_names(function_def.args))

    assert params == expected_names
