"""Tests the `importer.import_module` function"""
import pytest

from sphinx_ast_autodoc.importer import import_module


def test_it_raises_import_error_on_syntax_errors(mocker):
    """Test that it loads code from a module path"""

    code = """def fun(a,,b): pass"""

    mocker.patch("sphinx_ast_autodoc.importer.locate_module")
    load_module_code = mocker.patch("sphinx_ast_autodoc.importer.load_module_code")
    load_module_code.return_value = code

    with pytest.raises(ImportError):
        import_module("module_name")
