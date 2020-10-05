"""Module for model class.
"""

import inflection

from .field import Field


class Model(type):
    """The model metaclass. Allows to model classes for each existing tables when
    loading the schema."""

    def __new__(cls, schema):
        name = cls.to_singularized_pascal_case(schema["name"])
        class_ = super(Model, cls).__new__(cls, name, (), {})
        class_._schema = schema
        class_._id = schema["id"]
        class_._name = schema["name"]
        class_._primary_field = schema["primaryColumnName"]

        # Creating class properties.
        cls._add_property(
            class_,
            "schema",
            "_schema",
            doc="The schema of the table corresponsing to this model.",
        )
        cls._add_property(
            class_,
            "id",
            "_id",
            doc="The id of the table corresponsing to this model.",
        )
        cls._add_property(
            class_,
            "name",
            "_name",
            doc="The name of the table corresponsing to this model.",
        )
        cls._add_property(
            class_,
            "primary_field",
            "_primary_field",
            doc="The primary field name of the table corresponsing to this model.",
        )

        # Creating field properties.
        # We use the Airtable front facing "field" terminology in this API.
        for field_schema in schema["columns"]:
            # Snake casing the field name for the property.
            property_name = cls.to_snake_case(field_schema["name"])
            setattr(class_, property_name, Field(field_schema))

        return class_

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
    def to_singularized_pascal_case(name):
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
