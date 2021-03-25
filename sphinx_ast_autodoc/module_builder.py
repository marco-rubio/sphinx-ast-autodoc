"""Provides types and functionality for holding the extracted code information"""
import ast

from . import utils


class ModuleBuilder(ast.NodeVisitor):
    """Visits all the nodes from an AST"""

    def __init__(self, module):
        self._module = module

    def visit_Module(self, node):  # pylint: disable=invalid-name
        """Visits a module node"""

        setattr(self._module, "__doc__", ast.get_docstring(node))
        self.generic_visit(node)

    def visit_FunctionDef(self, node):  # pylint: disable=invalid-name
        """Visits a function function"""

        setattr(self._module, node.name, Function(node))
        self.generic_visit(node)


class CodeObject:  #  pylint: disable=too-few-public-methods
    """Base abstraction for parsed objects"""

    __doc__: str = None


class Module(CodeObject):  #  pylint: disable=too-few-public-methods
    """Provides an abstraction for a real module"""


class Function(CodeObject):  #  pylint: disable=too-few-public-methods
    """Provides an abstraction for a real module level function"""

    def __init__(self, node):
        """Initializes with the data from the node"""

        self.__doc__ = ast.get_docstring(node)
        self._node = node

    def get_signature(self, **kwargs):
        """Retrieves the signature for this function object"""

        return utils.get_function_signature(self._node, **kwargs)


def build_module(module_node: ast.Module) -> Module:
    """Creates a module from AST"""

    module = Module()

    visitor = ModuleBuilder(module)
    visitor.visit(module_node)

    return module
