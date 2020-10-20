"""Setup for airstorm.
"""

import os
import sys

from setuptools import setup

dirname = os.path.dirname(__file__)
sys.path.append(dirname)
import airstorm  # noqa: E402 pylint: disable=C0413

# Get the long description from the README file.
with open(os.path.join(dirname, "README.md"), encoding="utf-8") as fle:
    long_description = fle.read()

setup(
    name=airstorm.__name__,
    version=airstorm.__version__,
    description="A Python ORM for Airtable.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/playsthetic/airstorm",
    author=airstorm.__author__,
    author_email=airstorm.__email__,
    license=airstorm.__license__,
    packages=["airstorm"],
    install_requires=[
        "airtable-python-wrapper~=0.15",
        "inflection~=0.5",
    ],
    extras_require={
        "ci": [
            "flake8-print~=3.1",
            "flake8~=3.8",
            "pep8-naming~=0.11",
            "pytest-cov~=2.10.1",
            "pytest-html~=2.1.1",
            "pytest-pep8~=1.0.6",
            "pytest~=6.1.1",
            "requests-mock~=1.8",
            "sphinx-markdown-tables~=0.0",
            "sphinx-rtd-theme~=0.5",
            "sphinxcontrib-apidoc~=0.3",
            "Sphinx~=3.2",
        ],
    },
    include_package_data=True,
)
