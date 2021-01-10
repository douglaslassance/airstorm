import logging

from collections.abc import Iterable
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
        self.__doc__ = field.__doc__

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # If this field has a symmetric field we will make sure we get all necessary
        # records as one select.
        symmetric_model = self._field.symmetric_field()._model
        # This optimization is not necessary if the model is indexed as all
        # records would already have been selected.
        if not symmetric_model._indexed:
            ids = set()
            for record in instance:
                field = getattr(type(record), self._field._attribute_name)
                ids.update(field.raw_value(record))
            # Making sure we only select records that have not been already cached.
            ids = [_ for _ in ids if _ not in symmetric_model._cache]
            if ids:
                formula = 'SEARCH(RECORD_ID(), "{}")'.format(",".join(ids))
                logging.info("Performing pre-select.")
                symmetric_model._cache.select(formula=formula)

        values = []
        for record in instance:
            values.append(getattr(record, self._field._attribute_name))
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
