"""Tests the `importer.load_module_code` function"""
from sphinx_ast_autodoc.importer import load_module_code


def test_it_loads_code_from_a_module_path(mocker):
    """Test that it loads code from a module path"""

    code = """def fun(a): pass"""

    mock_open = mocker.mock_open(read_data=code)
    mocker.patch("sphinx_ast_autodoc.importer.open", mock_open)

    retrieved_code = load_module_code("module_path")
    assert retrieved_code == code
