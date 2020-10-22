import logging
import inflection

from .fields import Field
from .field_lists import FieldList


class ModelList(type):
    def __new__(cls, name, bases, dict_):
        # pylint: disable=protected-access

        def __init__(self, records=None):  # noqa: N807
            records = records or []
            for record in records:
                if not isinstance(record, self._model):
                    message = "{} can only initialize with a list of {}."
                    raise ValueError(message.format(type(self), self._model))
            list.__init__(self, records)

        def __del__(self):
            """TODO: Delete records in Airtable."""
            logging.warn("Not implemented yet.")

        def push(self):
            """ TODO: Push records changes to Airtable."""
            logging.warn("Not implemented yet.")

        def revert(self):
            """TODO: Revert records local changes."""
            logging.warn("Not implemented yet.")

        def grouped(self, field: Field):
            """Return records grouped by a field value."""
            grouped = {}
            for record in self:
                value = getattr(record, field._attribute_name)
                grouped.setdefault(value, type(self)()).append(record)
            return grouped

        def filtered(self, field: Field, value):
            """Returns record that match a specific field value.

            Args:
                field (Field): The field to filter by.
                value (TYPE): Description

            Returns:
                airstorm.model_list.ModelList: The filtered model list.
            """
            filtered = type(self)()
            for record in self:
                if getattr(record, field._attribute_name) == value:
                    filtered.append(record)
            return filtered

        def split(self, field: Field, value):
            """Returns two sets separtated by their matching state of a field value."""
            true = type(self)()
            false = type(self)()
            for record in self:
                if getattr(record, field._attribute_name) == value:
                    true.append(record)
                else:
                    false.append(record)
            return true, false

        def sorted(self, field: Field, reverse=False):
            """Return the list sorted by field."""
            # pylint: disable=redefined-builtin, no-value-for-parameter
            # pylint: disable=unexpected-keyword-arg
            return type(self)(
                sorted(
                    self,
                    key=lambda x: getattr(x, field._attribute_name),
                    reverse=reverse,
                )
            )

        methods = {
            "__init__": __init__,
            "__del__": __del__,
            "revert": revert,
            "push": push,
            "grouped": grouped,
            "filtered": filtered,
            "split": split,
        }
        dict_.update(methods)

        class_ = super(ModelList, cls).__new__(cls, name, bases, dict_)
        class_._model._base._model_list_by_id[class_._model._id] = class_

        # Looping throught the model fields and creating FieldList "properties" for the
        # class.
        for attribute_name in dir(class_._model):
            field = getattr(class_._model, attribute_name)
            if isinstance(field, Field):
                setattr(class_, inflection.pluralize(attribute_name), FieldList(field))
        return class_

    def find(cls, formula):
        """Return records with specific field value."""
        print(100, cls._model.id, field._id, value)
