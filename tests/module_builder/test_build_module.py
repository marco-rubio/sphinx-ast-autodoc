"""Tests the `module_builder.build_module` function"""
from sphinx_ast_autodoc.module_builder import build_module


def test_it_visits_the_received_ast_module_and_returns_built_module(mocker):
    """Test that it visits the received ast.Module node and returns the built module"""

    node = mocker.Mock()

    Module = mocker.patch("sphinx_ast_autodoc.module_builder.Module")
    Module.return_value = mocker.sentinel.module_object

    ModuleBuilder = mocker.patch("sphinx_ast_autodoc.module_builder.ModuleBuilder")

    module = build_module(node)
    assert ModuleBuilder.called_with(mocker.sentinel.module_object)
    assert ModuleBuilder.visit.called_with(node)
    assert module == mocker.sentinel.module_object
