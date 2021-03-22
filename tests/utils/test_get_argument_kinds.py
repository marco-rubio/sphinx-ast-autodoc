"""Tests for the `utils.get_argument_kinds` function"""
import ast
import inspect

import pytest

from sphinx_ast_autodoc.utils import get_argument_kinds

EMPTY_VALUE = inspect.Parameter.empty

POSITIONAL_ONLY = inspect.Parameter.POSITIONAL_ONLY
POSITIONAL_OR_KEYWORD = inspect.Parameter.POSITIONAL_OR_KEYWORD
KEYWORD_ONLY = inspect.Parameter.KEYWORD_ONLY
VAR_POSITIONAL = inspect.Parameter.VAR_POSITIONAL
VAR_KEYWORD = inspect.Parameter.VAR_KEYWORD


@pytest.mark.parametrize(
    "code,expected_kinds",
    [
        ["""def fun(a): pass""", [POSITIONAL_OR_KEYWORD]],
        ["""def fun(a, b): pass""", [POSITIONAL_OR_KEYWORD] * 2],
        ["""def fun(a, b, /): pass""", [POSITIONAL_ONLY] * 2],
        [
            """def fun(a, b, /, c): pass""",
            [POSITIONAL_ONLY, POSITIONAL_ONLY, POSITIONAL_OR_KEYWORD],
        ],
        [
            """def fun(a, b, *args): pass""",
            [POSITIONAL_OR_KEYWORD, POSITIONAL_OR_KEYWORD, VAR_POSITIONAL],
        ],
        [
            """def fun(a, b, *, c): pass""",
            [POSITIONAL_OR_KEYWORD, POSITIONAL_OR_KEYWORD, KEYWORD_ONLY],
        ],
        [
            """def fun(a, b, /, c, *, d): pass""",
            [POSITIONAL_ONLY, POSITIONAL_ONLY, POSITIONAL_OR_KEYWORD, KEYWORD_ONLY],
        ],
        [
            """def fun(a, b, /, c, *, d, **ops): pass""",
            [
                POSITIONAL_ONLY,
                POSITIONAL_ONLY,
                POSITIONAL_OR_KEYWORD,
                KEYWORD_ONLY,
                VAR_KEYWORD,
            ],
        ],
    ],
)
def test_it_processes_argument_kinds_correctly(code, expected_kinds):
    """Tests that it processes argument names correctly"""

    function_def = ast.parse(code).body[0]
    kinds = list(get_argument_kinds(function_def.args))

    assert kinds == expected_kinds
