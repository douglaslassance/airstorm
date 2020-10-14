"""Module holding the model class.
"""

import logging

from .cache import Cache
from .field import Field
from .functions import to_snake_case


class Model(type):
    """The model metaclass. Allows to model classes for each existing tables when
    loading the schema."""

    def __new__(cls, name, bases, dict_):
        """See type.__new__ documentation."""
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
            return bool(self._record_id)

        def __eq__(self, other):  # noqa: N807
            if isinstance(other, type(self)):
                return self._record_id == other._record_id
            return False

        methods = {
            "__init__": __init__,
            "__str__": __str__,
            "__bool__": __bool__,
            "__eq__": __eq__,
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

        model = super(Model, cls).__new__(cls, name, bases, dict_)
        model._base._model_by_id[dict_["_schema"]["id"]] = model

        logging.info(" ".join([name, model._base._id, model._base._api_key, model._id]))
        model._cache = Cache(
            model._base._id, model._base._api_key, model._id, index=dict_["_indexed"]
        )

        # Creating field (column) attributes.
        for field_schema in model._schema["columns"]:
            # Snake casing the field name for the attribute name..
            attribute_name = to_snake_case(field_schema["name"])
            # Informing of any field name conflicts. Technically Airtable allows to have
            # multiple column with the same name, but our API cannot support it for
            # obvious reason. As the result first arrived, first served.
            if hasattr(model, attribute_name):
                msg = 'Attribute "{}" on {} is already reserved.'
                msg = msg.format(attribute_name, model)
                logging.warning(msg)
            setattr(model, attribute_name, Field(model, field_schema))

        return model

    @classmethod
    def _add_property(cls, class_: object, name: str, attr: str, doc=""):
        """Adds a property to a class.

        Args:
            class_ (type): The class on which we add this property.
            name (str): The name for the property.
            attr (str): The attribute that property is affecting.
            docs (str, optional): The docstring for this property.
        """
        setattr(
            class_,
            name,
            property(
                fget=lambda class_: getattr(class_, attr),
                doc=doc,
            ),
        )
