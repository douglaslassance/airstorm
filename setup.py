"""Setup for airstorm.
"""

import os
import sys

from setuptools import setup

sys.path.append(os.path.dirname(__file__))
import airstorm  # noqa: E402 pylint: disable=C0413

setup(
    name="airstorm",
    version=airstorm.__version__,
    description="A Python ORM for Airtable.",
    url="https://github.com/playsthetic/airstorm",
    author="Douglas Lassance",
    author_email="douglassance@gmail.com",
    license="MIT",
    packages=["airstorm"],
    install_requires=[
        "airtable-python-wrapper~=0.15.1",
        "inflection~=0.5.1",
    ],
    extras_require={
        "ci": [
            "flake8~=3.8.4",
            "pytest-cov~=2.10.1"
            "pytest-html~=2.1.1"
            "pytest-pep8~=1.0.6"
            "pytest~=6.1.1"
            "recommonmark~=0.6.0",
            "Sphinx~=3.2.1",
            "sphinx-markdown-tables~=0.0.15",
            "sphinx-rtd-theme~=0.5.0",
        ],
    },
    include_package_data=True,
)
