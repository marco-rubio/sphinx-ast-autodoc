"""Provides documenters for the different object types available """
from sphinx.ext import autodoc
from sphinx.ext.autodoc.mock import ismock, mock, undecorate
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.inspect import stringify_signature

from sphinx_ast_autodoc import importer

logger = logging.getLogger(__name__)


class ASTCodeImporterMixin:
    """Provides AST base code importing"""

    # pylint: disable=too-few-public-methods

    def import_object(self, raiseerror: bool = False) -> bool:
        """Overrides the default object importing method"""

        success = False

        with mock(self.config.autodoc_mock_imports):
            try:
                ret = importer.import_object(
                    self.modname,
                    self.objpath,
                    self.objtype,
                    attrgetter=self.get_attr,
                    warningiserror=self.config.autodoc_warningiserror,
                )

                self.module, self.parent, self.object_name, self.object = ret

                if ismock(self.object):
                    self.object = undecorate(self.object)

                success = True

            except ImportError as exc:
                if raiseerror:
                    raise

                logger.warning(exc.args[0], type="autodoc", subtype="import_object")
                self.env.note_reread()
                success = False

        return success


class FunctionDocumenter(ASTCodeImporterMixin, autodoc.FunctionDocumenter):
    """Documents a function"""

    def format_args(self, **kwargs) -> str:
        """Formats the arguments from the function object"""

        if self.config.autodoc_typehints in ("none", "description"):
            kwargs.setdefault("show_annotation", False)

        try:
            self.env.app.emit("autodoc-before-process-signature", self.object, False)

            sig = self.object.get_signature(
                type_aliases=self.config.autodoc_type_aliases
            )

            args = stringify_signature(sig, **kwargs)

        except TypeError as exc:
            logger.warning(
                __("Failed to get a function signature for %s: %s"), self.fullname, exc
            )
            return None

        except ValueError:
            args = ""

        if self.config.strip_signature_backslash:
            args = args.replace("\\", "\\\\")

        return args
