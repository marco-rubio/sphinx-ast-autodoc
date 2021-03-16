"""Tests for the `utils.pad_defaults_list` function"""
import inspect

import pytest

from sphinx_ast_autodoc.utils import pad_defaults_list

EMPTY_VALUE = inspect.Parameter.empty


@pytest.mark.parametrize(
    "default_list,expected_length,expected_list",
    [
        [[], 5, [EMPTY_VALUE] * 5],
        [[1, 2, 3], 5, [EMPTY_VALUE, EMPTY_VALUE, 1, 2, 3]],
        [[1, 2, 3], 3, [1, 2, 3]],
    ],
)
def test_it_pads_lists_correctly(default_list, expected_length, expected_list):
    """Tests that is pads the input lists correctly"""

    result = list(pad_defaults_list(default_list, expected_length))
    assert len(result) == expected_length

    expected_padding = expected_length - len(default_list)
    assert result[0:expected_padding] == [EMPTY_VALUE] * expected_padding
    assert result[expected_padding:] == default_list
