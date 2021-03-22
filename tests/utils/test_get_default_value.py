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
    [
        [mock.Mock()],
        [str()],
    ],
)
def test_it_raises_value_error_for_unsupported_nodes(node):
    """Tests that is raises ValueError for unsupported node types"""

    with pytest.raises(ValueError):
        get_default_value(node)


def test_it_raises_not_implemented_for_unsupported_name_nodes():
    """Tests that is raises NotImplementedError for unsupported ast.Name nodes"""

    with pytest.raises(NotImplementedError):
        get_default_value(ast.Name())
