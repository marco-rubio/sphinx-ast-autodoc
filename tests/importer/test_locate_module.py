"""Tests the `importer.locate_module` function"""
import pytest

from sphinx_ast_autodoc.importer import locate_module


def test_it_raises_import_error_if_the_module_cannot_be_found(mocker):
    """Test it raises ImportError if the module cannot be found"""

    exists = mocker.patch("sphinx_ast_autodoc.importer.os.path.exists")
    exists.return_value = False

    with pytest.raises(ImportError):
        locate_module("some_module")


def test_it_returns_the_path_for_a_module_when_found(mocker):
    """Tests that it returns the path for a module when found"""

    sys = mocker.patch("sphinx_ast_autodoc.importer.sys")
    sys.path = ["one", "two", "three"]
    module_name = "some_module"

    exists = mocker.patch("sphinx_ast_autodoc.importer.os.path.exists")
    exists.return_value = True  #  side_effect = lambda path: expected_path in path

    expected_path = f"{sys.path[0]}/{module_name}.py"

    path = locate_module(module_name)
    assert expected_path == path
