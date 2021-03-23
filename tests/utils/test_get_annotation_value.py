"""Tests the `utils.get_annotation_value` function"""
import ast
from unittest import mock

import pytest

from sphinx_ast_autodoc.utils import get_annotation_value


@pytest.mark.parametrize(
    "node,expected",
    [
        [ast.Constant(value=1), 1],
        [ast.Constant(value=1.0), 1.0],
        [ast.Constant(value="A"), "A"],
        [ast.Constant(value=False), False],
        [ast.Constant(value=None), None],
        [ast.Name(id="identifier"), "identifier"],
    ],
)
def test_it_processes_supported_nodes(node, expected):
    """Tests that it processes supported nodes correctly"""

    actual = get_annotation_value(ast.arg(annotation=node))
    assert actual == expected


@pytest.mark.parametrize(
    "node",
    [
        ast.arg(annotation=mock.Mock()),
        ast.arg(annotation=str()),
    ],
)
def test_it_logs_errors_for_unsupported_node_types(mocker, node):
    """Tests that it logs an error for unsupported node types"""

    logger = mocker.patch("sphinx_ast_autodoc.utils.logger")

    get_annotation_value(node)
    assert logger.error.called is True


def test_it_logs_warnings_for_unsupported_subscript_nodes(mocker):
    """Tests that it logs a warning for unsupported ast.Subscript nodes"""

    logger = mocker.patch("sphinx_ast_autodoc.utils.logger")
    node = ast.arg(annotation=ast.Subscript())

    get_annotation_value(node)
    assert logger.warning.called is True
