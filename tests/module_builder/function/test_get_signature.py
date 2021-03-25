"""Tests for the `module_builder.Function.get_signature` method"""
from sphinx_ast_autodoc.module_builder import Function


def test_it_returns_generated_signature(mocker):
    """Test that it returns the generated signature"""

    get_signature = mocker.patch(
        "sphinx_ast_autodoc.module_builder.utils.get_function_signature"
    )
    get_signature.return_value = "function signature"

    # We patch ast.get_docstring because it doesn't like mocks
    get_docstring = mocker.patch("ast.get_docstring")
    get_docstring.return_value = "Docstring"

    function = Function(mocker.Mock())

    assert function.get_signature() == get_signature.return_value
