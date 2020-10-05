"""This module holds test for the database class.
"""
# pylint: disable=C0116

import os

from airstorm.base import Base
from airstorm.model import Model


def test_to_snake_case():
    for name in (
        "FooBar",
        "FooBar",
        "Foo Bar",
        "foo bar",
        "fooBar",
        "FOO_BAR",
        "FOO BAR",
        "foo_bar",
    ):
        conversion = Model.to_snake_case(name)
        assert conversion == "foo_bar", '"{}" > "{}"'.format(name, conversion)


def test_to_pascal_case():
    for name in (
        "FooBar",
        "FooBar",
        "Foo Bar",
        "foo bar",
        "fooBar",
        "FOO_BAR",
        "FOO BAR",
        "foo_bar",
        "FooBars",
        "FooBars",
        "Foo Bars",
        "foo bars`",
        "fooBars",
        "FOO_BARS",
        "FOO BARS",
        "foo_bars",
    ):
        conversion = Model.to_singularized_pascal_case(name)
        assert conversion == "FooBar", '"{}" > "{}"'.format(name, conversion)


def test_creating_models():
    dirname = os.path.dirname(__file__)
    base = Base("", "", os.path.join(dirname, "resources", "schema.json"))
    has_model_attr = False
    for attr in dir(base):
        if isinstance(getattr(base, attr), Model):
            has_model_attr = True
            break
    assert has_model_attr, "Was not able to create model types."


def test_creating_fields():
    dirname = os.path.dirname(__file__)
    base = Base("", "", os.path.join(dirname, "resources", "schema.json"))
    has_model_attr = False
    for attr in dir(base):
        if isinstance(getattr(base, attr), Model):
            has_model_attr = True
            break
    assert has_model_attr, "Was not able to create model types."
