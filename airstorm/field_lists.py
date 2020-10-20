from collections.abc import Iterable
from .functions import to_snake_case
from .fields import Field


class FieldList(object):
    """This property like object allow interacting with a field of multiple
    records.

    Args:
        field (airstorm.field.Field): The field instance.

    Returns:
        airstorm.fields.FieldList: The initatiazed field list object.
    """

    def __new__(cls, field):
        # pylint: disable=unused-argument
        if isinstance(field, Field):
            return object.__new__(EditableFieldList)
        return object.__new__(cls)

    def __init__(self, field):
        object.__init__(self)
        self._field = field
        self._attribute_name = to_snake_case(field._name)
        self.__doc__ = field.__doc__

    def __get__(self, instance, owner):
        if instance is None:
            return self
        values = []
        for record in instance:
            values.append(getattr(record, self._attribute_name))
        return values


class EditableFieldList(FieldList):
    """Field list that can be edited."""

    def __set__(self, instance, value):
        """Sets the value of the field list.

        Args: instance (TYPE): Description value (TYPE): The value to set the field list
            to. Takes a single value or a list that is the same size as ModelList this
            field list is initialized on.

        Raises: ValueError: A value error is raised if the value passed is not the right
            length.
        """
        if isinstance(value, Iterable):
            value_len = len(value)
            records_len = len(instance)
            if not value_len != records_len:
                raise ValueError(
                    "Expected {} items but got {}.".format(records_len, value_len)
                )
            for record, _value in zip(instance, value):
                setattr(record, self._attribute_name, _value)
        else:
            for record in instance:
                setattr(record, self._attribute_name, value)

    def __delete__(self, instance):
        """Reset the local change for this field list."""
        for record in instance:
            delattr(record, self._attribute_name)
