"""Setup for airstorm.
"""

import os
import sys

from setuptools import setup

dirname = os.path.dirname(__file__)
sys.path.append(dirname)
import airstorm  # noqa: E402 pylint: disable=C0413

# Get the long description from the README file.
with open(os.path.join(dirname, "README.md")) as fle:
    long_description = fle.read()

setup(
    name=airstorm.__name__,
    version=airstorm.__version__,
    description=airstorm.__doc__,
    long_description=long_description,
    url="https://github.com/playsthetic/airstorm",
    author=airstorm.__author__,
    author_email=airstorm.__email__,
    license=airstorm.__license__,
    packages=["airstorm"],
    install_requires=[
        "airtable-python-wrapper~=0.15.1",
        "inflection~=0.5.1",
    ],
    extras_require={
        "ci": [
            "flake8~=3.8",
            "flake8-print~=3.1",
            "pep8-naming~=0.11",
            "pytest-cov~=2.10.1"
            "pytest-html~=2.1.1"
            "pytest-pep8~=1.0.6"
            "pytest~=6.1.1"
            "Sphinx~=3.2",
            "sphinx-markdown-tables~=0.0",
            "sphinxcontrib-apidoc~=0.3",
            "sphinx-rtd-theme~=0.5",
        ],
    },
    include_package_data=True,
)
