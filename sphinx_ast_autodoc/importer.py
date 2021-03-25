"""Provides import utility functions"""
import ast
import os
import sys
import typing


def locate_module(
    module_name: str, warning_is_error: bool = False
) -> typing.Optional[str]:
    """Locates a module in the path"""
    #  pylint: disable=unused-argument

    module_path = None
    relative_path = module_name.replace(".", os.path.sep)
    filename = f"{relative_path}.py"

    for base in sys.path:
        if module_path is not None:
            continue

        current_path = os.path.join(base, filename)

        if os.path.exists(current_path):
            module_path = current_path

    if module_path is None:
        raise ImportError()

    return module_path


def load_module_code(module_path: str, warning_is_error: bool = False) -> str:
    """Loads the module code as a string"""
    #  pylint: disable=unused-argument

    module_code = ""

    with open(module_path, "r") as file:
        module_code = file.read()

    return module_code


def import_module(
    module_name: str, warningiserror: bool = False
) -> typing.Optional[module_builder.Module]:
    """Imports modules without executing them"""
    #  pylint: disable=unused-argument

    module_path = locate_module(module_name)
    module_code = load_module_code(module_path)

    try:
        ast_module = ast.parse(module_code, filename=module_path)

    except SyntaxError as error:
        raise ImportError() from error

    return module_builder.build_module(ast_module)
