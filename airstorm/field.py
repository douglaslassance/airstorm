"""Module holding the field class.
"""


class Field:
    """Airtable table field."""

    _read_only_field_types = ("formula", "computation")

    def __new__(cls, schema):
        if schema["type"] in cls._read_only_field_types:
            return object.__new__(cls)
        return object.__new__(EditableField)

    def __init__(self, schema):
        self._schema = schema
        self._value = 5

    def __get__(self, instance, owner):
        return self._value


class EditableField(Field):
    # pylint: disable=R0903
    """Field that can be both read and written.

    TODO: Implement __delete__ as a way to drop local changes.
    """

    def __new__(cls, schema):
        if schema["type"] in cls._read_only_field_types:
            raise Exception("{} is a read only field.".format(schema["name"]))
        return super(cls, Field).__new__(schema)

    def __set__(self, instance, value):
        self._value = value
