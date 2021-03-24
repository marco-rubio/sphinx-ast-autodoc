"""Provides types and functionality for holding the extracted code information"""
from . import utils

class CodeObject:  #  pylint: disable=too-few-public-methods
    """Base abstraction for parsed objects"""

    __doc__: str = None


class Function(CodeObject):  #  pylint: disable=too-few-public-methods
    """Provides an abstraction for a real module level function"""

    def __init__(self, node):
        """Initializes with the data from the node"""

        self.__doc__ = ast.get_docstring(node)
        self._node = node

    def get_signature(self, **kwargs):
        """Retrieves the signature for this function object"""

        return utils.get_function_signature(self._node, **kwargs)
