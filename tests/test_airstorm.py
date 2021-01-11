"""This module holds test for the database class.
"""
# pylint: disable=protected-access, missing-function-docstring

import os
import json

from airstorm.base import Base
from airstorm.model import Model
from airstorm.model_list import ModelList
from airstorm.fields import Field
from airstorm.field_lists import FieldList
from airstorm.functions import to_snake_case, to_singular_pascal_case

DIRNAME = os.path.dirname(__file__)
with open(os.path.join(DIRNAME, "resources", "schema.json")) as SCHEMA_FILE:
    SCHEMA = json.loads(SCHEMA_FILE.read())


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
        conversion = to_snake_case(name)
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
        conversion = to_singular_pascal_case(name)
        assert conversion == "FooBar", '"{}" > "{}"'.format(name, conversion)


def test_load_schema():
    base = Base("", "", SCHEMA)

    # Asserting models.
    loaded = False
    for attr in dir(base):
        model = getattr(base, attr)
        if isinstance(model, Model):
            for model_attr in dir(model):
                field = getattr(model, model_attr)
                if isinstance(field, Field):
                    loaded = True
                    break
        if loaded:
            break
    assert loaded, "Was not able to load models."

    # Asserting model lists.
    loaded = False
    for attr in dir(base):
        model_list = getattr(base, attr)
        if isinstance(model_list, ModelList):
            for model_list_attr in dir(model_list):
                field_list = getattr(model_list, model_list_attr)
                if isinstance(field_list, FieldList):
                    loaded = True
                    break
        if loaded:
            break
    assert loaded, "Was not able to load model lists."

    # Asserting attributes.
    assert base.Smoothy._id == "tblgeI1jinoGzStz2", "Cannot get model table ID."
    assert base.Fruit._id != "tblgeI1jinoGzStz2", "Models are sharing table IDs."
    assert base.Smoothy.name._id == "fldnl2M1LXxCNA0D7", "Getting field ID failed."


def test_access_data():
    # By filling the cache with dummy data we won't need to hit Airtable.
    # This is why we do not need to pass a base ID and API key.
    base = Base("", "", SCHEMA)
    _load_cache(base)
    smoothie = base.Smoothy("recxrTqISZmVBvDMs")
    assert smoothie.id == "recxrTqISZmVBvDMs", "Failed to initialize record data."
    assert smoothie.fruits.names == ["Apple", "Mango"], "Failed to field access data."


def _load_cache(base):
    with open(os.path.join(DIRNAME, "resources", "cache.json")) as cache_file:
        cache = json.loads(cache_file.read())

    for model_key in cache:
        model = getattr(base, model_key)
        model._indexed = True
        for key in cache[model_key]:
            model._cache[key] = cache[model_key][key]


def test_model_list():
    # By filling the cache with dummy data we won't need to hit Airtable.
    # This is why we do not need to pass a base ID and API key.
    base = Base("", "", SCHEMA)
    _load_cache(base)
    fruits = base.FruitList.find()
    assert fruits.grouped(base.Fruit.season) == {
        "Winter": base.FruitList(base.Fruit("recLSJFOqk6hYiWKg")),
        "Summer": base.FruitList(base.Fruit("recyEwR4TBE89mNsb")),
    }
