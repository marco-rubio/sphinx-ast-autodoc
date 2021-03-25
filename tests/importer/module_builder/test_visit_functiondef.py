"""Tests the `module_builder.ModuleBuilder.visit_FunctionDef` method"""
import ast

from sphinx_ast_autodoc.module_builder import Function, ModuleBuilder


def test_it_adds_the_member_to_the_module_and_retrieves_its_docstring(mocker):
    """
    Test that it adds the function as member of the module and retrieves the its
    docstring
    """

    docstring = "this is a docstring"
    function_name = "fun"
    module_code = ast.parse(
        f"""def {function_name}(a):
        "{docstring}"
    """
    )
    built_node = mocker.Mock()
    function_node = ast.parse(module_code).body[0]

    module_builder = ModuleBuilder(built_node)
    module_builder.visit_FunctionDef(function_node)

    generated_member = getattr(built_node, function_name)
    assert isinstance(generated_member, Function)
    assert generated_member.__doc__ == docstring
    assert generated_member._node == function_node
