"""Provides import utility functions"""
import ast
import os
import sys
import traceback
import typing
from typing import Any, Callable, List

from sphinx.ext.autodoc.importer import mangle
from sphinx.util import logging
from sphinx.util.inspect import safe_getattr

from . import module_builder

logger = logging.getLogger(__name__)


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


def import_object(
    module_name: str,
    object_path: List[str],
    objtype: str = "",
    attrgetter: Callable[[Any, str], Any] = safe_getattr,
    warningiserror: bool = False,
) -> Any:
    """Imports an object from a module"""
    # pylint: disable=too-many-locals, no-member, too-many-branches

    if object_path:
        logger.debug("[autodoc] from %s import %s", module_name, ".".join(object_path))

    else:
        logger.debug("[autodoc] import %s", module_name)

    try:
        module = None
        exc_on_importing = None
        object_path = list(object_path)

        while module is None:
            try:
                module = import_module(module_name, warningiserror=warningiserror)
                logger.debug("[autodoc] import %s => %r", module_name, module)

            except ImportError as exc:
                logger.debug("[autodoc] import %s => failed", module_name)
                exc_on_importing = exc
                if "." in module_name:
                    # retry with parent module
                    module_name, name = module_name.rsplit(".", 1)
                    object_path.insert(0, name)
                else:
                    raise

        obj = module
        parent = None
        object_name = None

        for attrname in object_path:
            parent = obj
            logger.debug("[autodoc] getattr(_, %r)", attrname)
            mangled_name = mangle(obj, attrname)
            obj = attrgetter(obj, mangled_name)
            logger.debug("[autodoc] => %r", obj)
            object_name = attrname
        return [module, parent, object_name, obj]
    except (AttributeError, ImportError) as exc:
        if isinstance(exc, AttributeError) and exc_on_importing:
            # restore ImportError
            exc = exc_on_importing

        if object_path:
            errmsg = "autodoc: failed to import %s %r from module %r" % (
                objtype,
                ".".join(object_path),
                module_name,
            )
        else:
            errmsg = "autodoc: failed to import %s %r" % (objtype, module_name)

        if isinstance(exc, ImportError):
            # import_module() raises ImportError having real exception obj and
            # traceback
            real_exc, traceback_msg = exc.args
            if isinstance(real_exc, SystemExit):
                errmsg += (
                    "; the module executes module level statement "
                    "and it might call sys.exit()."
                )
            elif isinstance(real_exc, ImportError) and real_exc.args:
                errmsg += "; the following exception was raised:\n%s" % real_exc.args[0]
            else:
                errmsg += "; the following exception was raised:\n%s" % traceback_msg
        else:
            errmsg += (
                "; the following exception was raised:\n%s" % traceback.format_exc()
            )

        logger.debug(errmsg)
        raise ImportError(errmsg) from exc
