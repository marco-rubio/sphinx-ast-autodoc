"""Tests the `module_builder.ModuleBuilder.visit_Module` method"""
import ast

from sphinx_ast_autodoc.module_builder import ModuleBuilder


def test_it_retrieves_the_module_docstring(mocker):
    """Test that it retrieves the module docstring"""

    docstring = "this is a docstring"
    module_code = ast.parse(f"""'''{docstring}'''""")
    built_node = mocker.Mock()

    module_builder = ModuleBuilder(built_node)
    module_builder.visit_Module(ast.parse(module_code))

    assert getattr(built_node, "__doc__") == docstring
