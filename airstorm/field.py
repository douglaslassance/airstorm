"""Module holding the field class.
"""


class Field:
    """Airtable field."""

    _read_only_field_types = ("formula", "computation")

    def __new__(cls, model, schema: dict):
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
        self.__doc__ = schema.get("description", "{} field.".format(schema["name"]))

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = (
            instance._cache.get(instance._record_id, {})
            .get("fields", {})
            .get(self._name)
        )
        if self._schema["type"] != "foreignKey":
            return value

        # If the field is of type foreign key we won't return the raw value.
        table_id = self._schema["typeOptions"]["foreignTableId"]
        model = instance._base._model_by_id[table_id]
        records = []
        value = value or []
        for id_ in value:
            records.append(model(id_))
        if self._schema["typeOptions"]["relationship"] == "one":
            return records[0] if records else model()
        return records


class EditableField(Field):
    """Field that can be edited.

    TODO: Implement __delete__ as a way to drop local changes.
    """

    def __new__(cls, model, schema: dict):
        if schema["type"] in cls._read_only_field_types:
            raise Exception("{} is a read only field.".format(schema["name"]))
        return super(cls, Field).__new__(schema)

    def __set__(self, instance, value):
        self._value = value

    def __delete__(self, instance):
        """Reset the local change for this field."""
        if instance is None:
            pass
        instance._value = None
