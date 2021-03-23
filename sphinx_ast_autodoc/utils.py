"""Provides import utility functions"""
import ast
import inspect
import itertools
import typing

from sphinx.util import logging

logger = logging.getLogger(__name__)


def pad_defaults_list(defaults_list, expected_length):
    """Pads a defaults list to match the expected length"""

    pad_count = expected_length - len(defaults_list)

    for value in itertools.chain([inspect.Parameter.empty] * pad_count, defaults_list):
        yield value


def get_argument_names(node: ast.arguments) -> typing.Iterable:
    """Gets the names for the arguments in an ast.arguments node"""

    for argument in itertools.chain(node.posonlyargs, node.args):
        yield argument.arg

    if node.vararg is not None:
        yield node.vararg.arg

    for argument in node.kwonlyargs:
        yield argument.arg

    if node.kwarg is not None:
        yield node.kwarg.arg


def get_argument_kinds(node: ast.arguments) -> typing.Iterable:
    """Gets the kinds for the arguments in an ast.arguments node"""

    for _ in node.posonlyargs:
        yield inspect.Parameter.POSITIONAL_ONLY

    for _ in node.args:
        yield inspect.Parameter.POSITIONAL_OR_KEYWORD

    if node.vararg is not None:
        yield inspect.Parameter.VAR_POSITIONAL

    for _ in node.kwonlyargs:
        yield inspect.Parameter.KEYWORD_ONLY

    if node.kwarg is not None:
        yield inspect.Parameter.VAR_KEYWORD


def get_default_value(
    node: typing.Union[ast.Constant, ast.Name, inspect.Parameter.empty, None]
):
    """Gets the value from a defaults node"""

    if isinstance(node, ast.Constant):
        value = node.value

    elif isinstance(node, ast.Name):
        value = inspect.Parameter.empty
        logger.warning(
            "get_default_value got an ast.Name node which isn't yet supported"
        )

    elif node in [None, inspect.Parameter.empty]:
        value = inspect.Parameter.empty

    else:
        value = inspect.Parameter.empty
        logger.error(f"get_default_value got an unsupported node of type {type(node)}")

    return value


def get_argument_defaults(node: ast.arguments) -> typing.Iterable:
    """Gets the defaults for the arguments in an ast.arguments node"""

    total_positional_arguments = len(node.posonlyargs) + len(node.args)
    positional_defaults = pad_defaults_list(node.defaults, total_positional_arguments)

    for default in positional_defaults:
        yield get_default_value(default)

    if node.vararg is not None:
        yield inspect.Parameter.empty

    for default in node.kw_defaults:
        yield get_default_value(default)

    if node.kwarg is not None:
        yield inspect.Parameter.empty


def get_annotation_value(node: typing.Union[ast.Name, ast.Constant, None]):
    """Gets the value from an annotation node"""

    annotation = node.annotation

    if isinstance(annotation, ast.Constant):
        value = annotation.value

    elif isinstance(annotation, ast.Name):
        value = annotation.id

    elif isinstance(annotation, ast.Subscript):
        value = inspect.Parameter.empty
        logger.warning(
            "get_annotation_value got an ast.Subscript node which isn't supported yet"
        )

    elif annotation is None:
        value = inspect.Parameter.empty

    else:
        value = inspect.Parameter.empty
        logger.error(
            f"get_annotation_value got an unsupported node of type {type(node)}"
        )

    return value


def get_argument_annotations(node: ast.arguments) -> typing.Iterable:
    """Gets the return typ annotations for the arguments in an ast.arguments node"""

    for argument in itertools.chain(node.posonlyargs, node.args):
        yield get_annotation_value(argument)

    if node.vararg is not None:
        yield inspect.Parameter.empty

    for argument in node.kwonlyargs:
        yield get_annotation_value(argument)

    if node.kwarg is not None:
        yield inspect.Parameter.empty


def get_parameters(
    node: ast.arguments,
) -> typing.List[typing.Optional[inspect.Parameter]]:
    """Gets the function's param list"""

    arguments = zip(
        get_argument_names(node),
        get_argument_kinds(node),
        get_argument_defaults(node),
        get_argument_annotations(node),
    )

    for name, kind, default, annotation in arguments:
        yield inspect.Parameter(
            name=name, kind=kind, default=default, annotation=annotation
        )


def get_return_annotation(
    node: typing.Union[ast.Constant, ast.Name, ast.Subscript, None],
) -> typing.Union[inspect.Signature.empty]:
    """Gets the return annotation from an ast.FunctionDef node"""

    if node is None:
        value = inspect.Signature.empty

    elif isinstance(node, ast.Constant):
        value = node.value

    elif isinstance(node, ast.Name):
        value = node.id

    elif isinstance(node, ast.Subscript):
        value = inspect.Signature.empty
        logger.warning(
            "get_return_annotation got an ast.Subscript node which is not yet supported"
        )

    else:
        value = inspect.Signature.empty
        logger.error(
            f"get_return_annotation got an unsupported node of type {type(node)}"
        )

    return value


def get_function_signature(node: ast.FunctionDef, **kwargs) -> inspect.Signature:
    """Gets a function signature from an ast.FunctionDef node"""
    # pylint: disable=unused-argument

    return inspect.Signature(
        get_parameters(node.args), return_annotation=get_return_annotation(node.returns)
    )
