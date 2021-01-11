import logging
import inflection

from .fields import Field
from .field_lists import FieldList


class ModelList(type):
    """The model list metaclass allows to generate model list classes for each existing
    tables when loading the schema."""

    def __new__(cls, name, bases, dict_):
        # pylint: disable=protected-access, too-many-locals

        def __init__(self, *records):  # noqa: N807
            records = records or []
            for record in records:
                if not isinstance(record, self._model):
                    message = "{} can only initialize with one or more {} arguments."
                    raise ValueError(message.format(type(self), self._model))
            list.__init__(self, records)

        def delete(self):  # noqa: N807
            """TODO: Delete records in Airtable."""
            # pylint: disable=unused-argument
            logging.warning("delete implemented yet.")

        def push(self):
            """ TODO: Push records changes to Airtable."""
            # pylint: disable=unused-argument
            logging.warning("push implemented yet.")

        def revert(self):
            """TODO: Revert records local changes."""
            # pylint: disable=unused-argument
            logging.warning("revert implemented yet.")

        def grouped(self, field: Field):
            """Return records grouped by a field value."""
            grouped = {}
            for record in self:
                values = getattr(record, field._attribute_name)
                if not isinstance(values, list):
                    values = [values]
                for value in values:
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

        def sorted_(self, field: Field, reverse=False):
            """Return the list sorted by field."""
            # pylint: disable=redefined-builtin, no-value-for-parameter
            # pylint: disable=unexpected-keyword-arg
            sorted_ = sorted(
                self,
                key=lambda record: getattr(record, field._attribute_name),
                reverse=reverse,
            )
            return type(self)(*sorted_)

        methods = {
            "__init__": __init__,
            "delete": delete,
            "revert": revert,
            "push": push,
            "grouped": grouped,
            "filtered": filtered,
            "split": split,
            "sorted": sorted_,
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

    def find(cls, formula=""):
        """Return records with specific field value.

        Args: formula (str, optional): A airtable formula to filter the search. Lean
            more about writing valid formulas at
            https://support.airtable.com/hc/en-us/articles/203255215-Formula-Field-Reference.

        Returns:
            airstorm.model_list.ModelList: The found records.
        """
        # pylint: disable=protected-access, no-value-for-parameter
        cache_records = cls._model._cache.select(formula=formula)
        records = []
        for id_ in cache_records:
            records.append(cls._model(id_))
        return cls(*records)
