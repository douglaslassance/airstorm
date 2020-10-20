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

        def grouped_by(self, field):
            """TODO: Return records grouped by a field value."""
            logging.warn("Not implemented yet.")

        def delete(self):
            """TODO: Delete records in Airtable."""
            logging.warn("Not implemented yet.")

        def push(self):
            """ TODO: Push records changes to Airtable."""
            logging.warn("Not implemented yet.")

        methods = {
            "__init__": __init__,
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
