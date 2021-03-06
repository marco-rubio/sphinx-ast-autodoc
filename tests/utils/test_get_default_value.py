"""Tests the utils.get_default_value function"""
import ast
from unittest import mock

import pytest

from sphinx_ast_autodoc.utils import get_default_value


@pytest.mark.parametrize(
    "node,expected",
    [
        [ast.Constant(value=1), 1],
        [ast.Constant(value=1.0), 1.0],
        [ast.Constant(value="A"), "A"],
        [ast.Constant(value=False), False],
        [ast.Constant(value=None), None],
    ],
)
def test_it_returns_the_value_of_a_constant_node(node, expected):
    """Tests that it returns the value for ast.Constant nodes"""

    actual = get_default_value(node)
    assert actual == expected


@pytest.mark.parametrize(
    "node",
    [mock.Mock(), str()],
)
def test_it_logs_errors_for_unsupported_node_types(mocker, node):
    """Tests that it logs an error for unsupported node types"""

    logger = mocker.patch("sphinx_ast_autodoc.utils.logger")

    get_default_value(node)
    assert logger.error.called is True


def test_it_logs_warnings_for_unsupported_name_nodes(mocker):
    """Tests that it logs a warning for unsupported ast.Name nodes"""

    logger = mocker.patch("sphinx_ast_autodoc.utils.logger")

    get_default_value(ast.Name())
    assert logger.warning.called is True
