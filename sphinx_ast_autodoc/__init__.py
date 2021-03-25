"""Initializes the main module"""
import sphinx
from sphinx.config import ENUM
from sphinx.ext.autodoc import migrate_autodoc_member_order

from sphinx_ast_autodoc import documenters

__version__ = "0.0.1"


def setup(app):
    """Sets up the extension"""

    app.add_autodocumenter(documenters.FunctionDocumenter)

    app.add_config_value(
        "autoclass_content", "class", True, ENUM("both", "class", "init")
    )
    app.add_config_value(
        "autodoc_member_order",
        "alphabetical",
        True,
        ENUM("alphabetic", "alphabetical", "bysource", "groupwise"),
    )
    app.add_config_value("autodoc_default_options", {}, True)
    app.add_config_value("autodoc_docstring_signature", True, True)
    app.add_config_value("autodoc_mock_imports", [], True)
    app.add_config_value(
        "autodoc_typehints", "signature", True, ENUM("signature", "description", "none")
    )
    app.add_config_value("autodoc_type_aliases", {}, True)
    app.add_config_value("autodoc_warningiserror", True, True)
    app.add_config_value("autodoc_inherit_docstrings", True, True)
    app.add_event("autodoc-before-process-signature")
    app.add_event("autodoc-process-docstring")
    app.add_event("autodoc-process-signature")
    app.add_event("autodoc-skip-member")

    app.connect("config-inited", migrate_autodoc_member_order, priority=800)

    app.setup_extension("sphinx.ext.autodoc.type_comment")
    app.setup_extension("sphinx.ext.autodoc.typehints")

    return {"version": sphinx.__display_version__, "parallel_read_safe": True}
