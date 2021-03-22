"""Tests the utils.get_parameters function"""
import ast
import inspect

import pytest

from sphinx_ast_autodoc.utils import get_parameters

EMPTY_VALUE = inspect.Parameter.empty


@pytest.mark.parametrize(
    "code,expected_annotations",
    [
        ["""def fun(a): pass""", [EMPTY_VALUE]],
        ["""def fun(a:str): pass""", ["str"]],
        ["""def fun(a:str, b:"int"): pass""", ["str", "int"]],
        ["""def fun(a:str, b:"int", *, c:bool): pass""", ["str", "int", "bool"]],
        ["""def fun(a:str, b:"int", *c): pass""", ["str", "int", EMPTY_VALUE]],
        ["""def fun(a:str, b:"int", **c): pass""", ["str", "int", EMPTY_VALUE]],
    ],
)
def test_it_processes_argument_annotations_correctly(code, expected_annotations):
    """Tests that it processes argument annotations correctly"""

    function_def = ast.parse(code).body[0]
    params = list(get_parameters(function_def.args))

    annotations = [param.annotation for param in params]
    assert annotations == expected_annotations
