import io
import os
import re
from collections import OrderedDict

from setuptools import find_packages, setup


def get_long_description():
    """Gets the package's long description"""

    for filename in ("README.md",):
        with io.open(filename, "r", encoding="utf-8") as f:
            yield f.read()


def get_version(package):
    """Gets the package's version"""

    with io.open(os.path.join(package, "__init__.py")) as f:
        pattern = r'^__version__ = [\'"]([^\'"]*)[\'"]'
        return re.search(pattern, f.read(), re.MULTILINE).group(1)


setup(
    name="sphinx-ast-autodoc",
    version=get_version("sphinx_ast_autodoc"),
    license="MIT",
    description="AST based Sphinx Autodoc extension replacement",
    long_description="\n\n".join(get_long_description()),
    author="marco-rubio",
    author_email="marco.rubio.dev@gmail.com",
    maintainer="marco-rubio",
    url="https://github.com/marco-rubio/sphinx-ast-autodoc",
    project_urls=OrderedDict(
        (
            (
                "Issues",
                "https://github.com/marco-rubio/sphinx-ast-autodoc/issues",
            ),
        )
    ),
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "Sphinx==3.5.2",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    zip_safe=False,
    tests_require=[
        "coverage==5.5",
        "pytest==6.2.2",
        "pytest-cov==2.11.1",
        "pytest-mock==3.5.1",
    ],
    package_data={},
)
