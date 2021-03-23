"""Tests for the `utils.get_return_annotation` function"""
import ast
import inspect

import pytest

from sphinx_ast_autodoc.utils import get_return_annotation


@pytest.mark.parametrize(
    "code, expected_type",
    [
        ["""def fun(a): pass""", inspect.Parameter.empty],
        ["""def fun(a) -> str: pass""", "str"],
        ["""def fun(a) -> "str": pass""", "str"],
        ["""def fun(a) -> typing.Optional[str]: pass""", inspect.Parameter.empty],
    ],
)
def test_it_processes_return_annotations(code, expected_type):
    """Tests that it processes return annotations correctly"""

    function_def = ast.parse(code).body[0]
    annotation = get_return_annotation(function_def.returns)

    assert annotation == expected_type


@pytest.mark.parametrize(
    "node",
    [
        "something",
        1,
        True,
    ],
)
def test_it_logs_errors_for_unsupported_node_types(mocker, node):
    """Tests that it logs an error for unsupported node types"""

    logger = mocker.patch("sphinx_ast_autodoc.utils.logger")

    get_return_annotation(node)
    assert logger.error.called is True


def test_it_logs_warnings_for_subscript_nodes(mocker):
    """Tests that it logs a warning for ast.Subscript nodes"""

    logger = mocker.patch("sphinx_ast_autodoc.utils.logger")

    get_return_annotation(ast.Subscript())
    assert logger.warning.called is True
