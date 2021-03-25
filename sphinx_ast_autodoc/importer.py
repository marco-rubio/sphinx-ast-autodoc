"""Provides import utility functions"""
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
