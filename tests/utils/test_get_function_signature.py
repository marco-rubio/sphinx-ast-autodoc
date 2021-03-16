"""Tests for the `utils.get_function_signature` function"""
import ast
import inspect

from sphinx_ast_autodoc.utils import get_function_signature


def test_it_returns_a_signature():
    """Tests that it retrieves corrects signatures"""

    code = """def func(a, b): pass"""
    func = ast.parse(code).body[0]

    assert isinstance(get_function_signature(func), inspect.Signature)


def test_it_retrieves_params_and_return_annotations(mocker):
    code = """def func(a, b): pass"""
    func = ast.parse(code).body[0]

    get_parameters = mocker.patch("sphinx_ast_autodoc.utils.get_parameters")
    get_return_annotation = mocker.patch(
        "sphinx_ast_autodoc.utils.get_return_annotation"
    )

    get_function_signature(func)

    get_parameters.assert_called_once_with(func.args)
    get_return_annotation.assert_called_once_with(func.returns)
