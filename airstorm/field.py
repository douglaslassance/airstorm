"""Module holding the field class.
"""


class Field:
    """Airtable table field."""

    _read_only_field_types = ("formula", "computation")

    def __new__(cls, model, schema):
        # pylint: disable=unused-argument
        """Summary

        Args:
            model (airstorm.model.Model): The model this field belongs to.
            schema (dict): The schema for this field.

        Returns:
            TYPE: Description
        """
        if schema["type"] in cls._read_only_field_types:
            return object.__new__(cls)
        return object.__new__(EditableField)

    def __init__(self, model, schema):
        self._schema = schema
        self._id = schema["id"]
        self._name = schema["name"]
        self._value = 5
        self._model = model

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._value

    @property
    def model(self):
        """The model this field belong to.

        Returns:
            airstorm.model.Model: The model this field belong to.
        """
        return self._model

    @property
    def schema(self):
        """The field schema.

        Returns:
            dict: The field schema.
        """
        return self._schema

    @property
    def name(self):
        """The Airtable field name.

        Returns:
            str: The Airtable field name.
        """
        return self._name

    @property
    def id(self):
        # pylint: disable=invalid-name
        """The Airtable field id.

        Returns:
            str: The Airtable field id.
        """
        return self._id


class EditableField(Field):
    """Field that can be edited.

    TODO: Implement __delete__ as a way to drop local changes.
    """

    def __new__(cls, model, schema):
        if schema["type"] in cls._read_only_field_types:
            raise Exception("{} is a read only field.".format(schema["name"]))
        return super(cls, Field).__new__(schema)

    def __set__(self, instance, value):
        self._value = value
