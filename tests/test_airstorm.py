"""This module holds test for the database class.
"""

import os

from airstorm import Base
from airstorm.model import Model
from airstorm.field import Field

DIRNAME = os.path.dirname(__file__)
SCHEMA = os.path.join(DIRNAME, "resources", "schema.json")


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


def test_to_singular_pascal_case():
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
        conversion = Model.to_singular_pascal_case(name)
        assert conversion == "FooBar", '"{}" > "{}"'.format(name, conversion)


def test_loaded_tables():
    base = Base("", "", SCHEMA)
    loaded_tables = False
    for model in dir(base):
        model = getattr(base, model)
        if isinstance(model, Model):
            for field in dir(model):
                field = getattr(model, field)
                if isinstance(field, Field):
                    loaded_tables = True
                    break
        if loaded_tables:
            break
    assert loaded_tables, "Was not able to load tables."


def test_dynamic_attributes():
    base = Base("", "", SCHEMA)
    assert base.Context.table_id == "tblCko8U7PjPYPNpf", "Cannot get model table ID."
    assert base.Asset.table_id != "tbl00YIV1HyHLE56A", "Models are sharing table IDs."
    assert base.Context.name.id == "fld5tR1r0jBCqjG06", "Getting field ID failed."
