"""Module holding the base class definition.
"""

from .model import Model
from .functions import to_singular_pascal_case


class Base:
    """The base class is the root object to access the airtable bases.

    During initialization the instance will be filled with attribute point to the
    different models available in the database.

    Args:
        base_id (str): The id of the Airtable base.
        api_key (str): The API key of the user that will connect the base.

        schema (str): A dictionary representing the schema.
            Use the following Gist to generate to generate the schema manually:
            https://gist.github.com/douglaslassance/0ba26f2cf2aa9bb21a521ba07d751244

        to_model_name (callable, optional): Transform table into model class names.

            By default it will PascalCase and singularize the name of the tables,
            but this argurment provide users with potentially desired flexibility.

        indexed_tables (list, collections.abc.Iterable): List of table names to
            index immediatly.

            This basically caches the entire table locally in a single request. It
            will make the base initialization a bit slower but in turn you won't
            ever need to hit the airtable for any record of this table. This is a
            fit optimization for tables with little records and that do not change
            often.
    """

    def __init__(
        self,
        base_id: str,
        api_key: str,
        schema: dict,
        to_model_name=to_singular_pascal_case,
        indexed_tables=None,
    ):
        object.__init__(self)

        self._id = base_id
        self._api_key = api_key
        self._schema = schema
        self._model_by_id = {}

        for table_schema in self._schema["tables"]:
            table_name = table_schema["name"]
            model_name = to_model_name(table_schema["name"])
            model_dict = {
                "_schema": table_schema,
                "_base": self,
                "_indexed": table_name in (indexed_tables or []),
            }
            setattr(self, model_name, Model(model_name, (), model_dict))
