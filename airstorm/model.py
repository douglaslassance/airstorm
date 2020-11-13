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

        def __repr__(self):  # noqa: N807
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

        def delete(self):  # noqa: N807
            """TODO: Delete record in Airtable."""
            logging.warning("delete implemented yet.")

        def push(self):
            """ TODO: Push record changes to Airtable."""
            logging.warning("push implemented yet.")

        def revert(self):
            """ TODO: Revert record local change."""
            logging.warning("revert implemented yet.")

        methods = {
            "__init__": __init__,
            "__repr__": __repr__,
            "__bool__": __bool__,
            "__eq__": __eq__,
            "delete": delete,
            "push": push,
            "revert": revert,
        }
        dict_.update(methods)

        attributes = {
            "_id": dict_["_schema"]["id"],
            "_name": dict_["_schema"]["name"],
            "_primary_field": dict_["_schema"]["primaryColumnName"],
            "_field_by_id": {},
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
        class_._cache = Cache(class_)

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
            field = Field(class_, field_schema)
            setattr(class_, attribute_name, field)
            class_._field_by_id[field_schema["id"]] = field

        return class_

    def find(cls, formula=""):
        """Return first found record by field value.

        Args: formula (str, optional): A airtable formula to filter the search. Lean
            more about writing valid formulas at
            https://support.airtable.com/hc/en-us/articles/203255215-Formula-Field-Reference.

        Returns:
            airstorm.model.Model: The found record.
        """
        records = cls._base._model_list_by_id[cls._schema["id"]].find(formula=formula)
        return records[0] if records else cls()
