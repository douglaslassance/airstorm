import logging

from .fields import Field
from .cache import Cache
from .functions import to_snake_case


class Model(type):
    """The model metaclass allows to generate model classes for each existing tables
    when loading the schema."""

    def __new__(cls, name, bases, dict_):
        # pylint: disable=protected-access

        def __init__(self, record_id=""):  # noqa: N807
            record = self._cache.get(record_id)
            self._record_id = record_id if record else ""

        def __str__(self):  # noqa: N807
            return '<{}("{}") {}>'.format(
                type(self).__name__,
                self._record_id,
                str(getattr(self, to_snake_case(self._primary_field))),
            )

        def __bool__(self):  # noqa: N807
            """Will return whether or not the record exists in Airtable.

            Returns:
                bool: Whether the record exists.
            """
            return bool(self._record_id)

        def __eq__(self, other):  # noqa: N807
            if isinstance(other, type(self)):
                return self._record_id == other._record_id
            return False

        def __del__(self):
            """TODO: Delete record in Airtable."""
            logging.warning("Not implemented yet.")

        def push(self):
            """ TODO: Push record changes to Airtable."""
            logging.warning("Not implemented yet.")

        def revert(self):
            """ TODO: Revert record local change."""
            logging.warning("Not implemented yet.")

        methods = {
            "__init__": __init__,
            "__str__": __str__,
            "__bool__": __bool__,
            "__eq__": __eq__,
            "__del__": __del__,
            "push": push,
            "revert": revert,
        }
        dict_.update(methods)

        attributes = {
            "_id": dict_["_schema"]["id"],
            "_name": dict_["_schema"]["name"],
            "_primary_field": dict_["_schema"]["primaryColumnName"],
            "__doc__": dict_["_schema"].get(
                "description", "{} model.".format(dict_["_schema"]["name"])
            ),
        }
        dict_.update(attributes)

        class_ = super(Model, cls).__new__(cls, name, bases, dict_)
        class_._base._model_by_id[dict_["_schema"]["id"]] = class_

        logging.info(
            " ".join([name, class_._base._id, class_._base._api_key, class_._id])
        )
        class_._cache = Cache(
            class_._base._id, class_._base._api_key, class_._id, index=dict_["_indexed"]
        )

        # Creating field (column) attributes.
        for field_schema in class_._schema["columns"]:
            # Snake casing the field name for the attribute name..
            attribute_name = to_snake_case(field_schema["name"])
            # Informing of any field name conflicts. Technically Airtable allows to have
            # multiple column with the same name, but our API cannot support it for
            # obvious reason. As the result first arrived, first served.
            if hasattr(class_, attribute_name):
                msg = 'Attribute "{}" on {} is already reserved.'
                msg = msg.format(attribute_name, class_)
                logging.warning(msg)
            setattr(class_, attribute_name, Field(class_, field_schema))

        return class_

    def find(self, formula):
        """ TODO: Return first found record by field value."""
        logging.warn("Not implemented yet.")
