"""Module holding the model class.
"""

import logging
import inflection

from .field import Field
from .cache import Cache

from airtable import Airtable


class Model(type):
    """The model metaclass. Allows to model classes for each existing tables when
    loading the schema."""

    def __new__(cls, name, bases, dict_):
        """See type.__new__ documentation."""
        # pylint: disable=protected-access

        def __init__(self, record_id=None):
            self._record = None
            if record_id:
                self._record = self.cache.setdefault(
                    record_id, self.airtable.get(record_id)
                )
                self._hydrate()

        def exists(self):
            return bool(self._record)

        def _hydrate(self):
            if self._record:
                for attr in dir(self):
                    field = getattr(self, attr)
                    if isinstance(field, Field):
                        if field.id in self._record.fields:
                            setattr(self, attr, self._record.fields[field.name])

        methods = {
            "__init__": __init__,
            "exists": exists,
            "_hydrate": _hydrate,
        }
        dict_.update(methods)

        attributes = {
            "_table_id": dict_["_schema"]["id"],
            "_table_name": dict_["_schema"]["name"],
            "_primary_field": dict_["_schema"]["primaryColumnName"],
            "_cache": Cache(),
            "_airtable": Airtable(
                dict_["_base"]._id,
                dict_["_schema"]["name"],
                dict_["_base"]._api_key,
            ),
        }
        dict_.update(attributes)

        model = super(Model, cls).__new__(cls, name, bases, dict_)

        # Add properties.
        for attr in attributes:
            cls._add_property(model, attr.strip("_"), attr)

        # Creating field (column) attributes.
        for field_schema in model._schema["columns"]:
            # Snake casing the field name for the attribute name..
            attribute_name = model.to_snake_case(field_schema["name"])
            # TODO: Find a way around conflits.
            if hasattr(model, attribute_name):
                msg = (
                    "Field {} is skipped. "
                    "Attribute airstorm.model.Model.{} is reserved."
                )
                msg = msg.format(field_schema["name"], attribute_name)
                logging.warning(msg)
            setattr(model, attribute_name, Field(model, field_schema))

        return model

    @classmethod
    def _add_property(cls, class_, name, attr, doc=None):
        """Adds a property to a class.

        Args:
            class_ (type): The class on which we add this property.
            name (str): The name for the property.
            attr (str): The attribute that property is affecting.
            docs (str, optional): The docstring for this property.
        """
        setattr(
            class_,
            name,
            property(
                fget=lambda class_: getattr(class_, attr),
                doc=doc,
            ),
        )

    @staticmethod
    def to_singular_pascal_case(name):
        """Make any name into a valid singulatized PascalCased name.

        Args:
            name (TYPE): The name to singularized PascalCase.

        Returns:
            str: The singularized PascalCased name.
        """
        return inflection.singularize(
            inflection.camelize(
                inflection.parameterize(inflection.titleize(name), separator="_")
            )
        )

    @staticmethod
    def to_snake_case(name):
        """Make any name into a valid snake_cased name.

        Args:
            name (str): The name to snake_case.

        Returns:
            TYPE: The snake_cased name.
        """
        return inflection.parameterize(inflection.titleize(name), separator="_").lower()


# class Model(metaclass=ModelType):
#     def __init__(self, record_id=None):
#         """Summary

#         Args:
#             record_id (None, optional): Description
#         """
#         self._record_id = record_id
#         record = self._cache.get(record_id)
#         if not record:
#             record = self._airtable.get(id)
#         if record:
#             self._hydrate(record)
#         print("INITIZALIZED")

#     def exists(self):
#         """Summary

#         Returns:
#             TYPE: Description
#         """
#         return bool(self._record_id in self._cache)

#     def _hydrate(self, record):
#         """Hydrate the field instance with the cache data."""
#         for attr in dir(self):
#             field = getattr(self, attr)
#             if isinstance(field, Field):
#                 field = record.fields.get(field.id, field.type())
