from .functions import to_snake_case


class Field:
    """This property like object will map against a table field exposed as a snake_cased
    attribute on the model.

    Args:
        model (airstorm.model.Model): The model this field belongs to.
        schema (dict): The schema for this field.

    Returns:
        airstorm.fields.Field: The initatiazed field object.
    """

    _read_only_field_types = ("formula", "computation")

    def __new__(cls, model, schema: dict):
        # pylint: disable=unused-argument
        if schema["type"] in cls._read_only_field_types:
            return object.__new__(cls)
        return object.__new__(EditableField)

    def __init__(self, model, schema):
        object.__init__(self)
        self._schema = schema
        self._id = schema["id"]
        self._name = schema["name"]
        self._value = 5
        self._model = model
        self._attribute_name = to_snake_case(self._name)
        self.__doc__ = schema.get("description", "{} field.".format(schema["name"]))

    def _default_value(self):
        type_ = self._schema["type"]
        if type_ == "number":
            format_ = self._schema["typeOptions"]["format"]
            return 0 if format_ == "interger" else 0.0
        if type_ in ("text", "singleSelect"):
            return ""
        if type_ == "multiSelect":
            return []
        return None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = (
            instance._cache.get(instance._record_id, {})
            .get("fields", {})
            .get(self._name, self._default_value())
        )

        if self._schema["type"] == "foreignKey":
            # If the field is of type foreign key we won't return the raw value.
            table_id = self._schema["typeOptions"]["foreignTableId"]
            model = instance._base._model_by_id[table_id]
            records = []
            value = value or []
            for id_ in value:
                records.append(model(id_))
            if self._schema["typeOptions"]["relationship"] == "one":
                return records[0] if records else model()
            model_list = self._model._base._model_list_by_id[model._id]
            return model_list(*records)

        return value


class EditableField(Field):
    """Field that can be edited."""

    def __new__(cls, model, schema: dict):
        if schema["type"] in cls._read_only_field_types:
            raise Exception("{} is a read only field.".format(schema["name"]))
        return super(cls, Field).__new__(schema)

    def __set__(self, instance, value):
        """Sets the value of the field.
        The value is "local" until the changes are pushed.
        """
        self._value = value

    def __delete__(self, instance):
        """Reset the local change for this field."""
        instance._value = None
