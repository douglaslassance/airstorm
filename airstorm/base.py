"""Module for base class.
"""

import json

from .model import Model


class Base:
    # pylint: disable=R0903
    """The base class is the root object to access the airtable base."""

    def __init__(self, id_, key, schema, renamer=lambda x: x):
        """Intialize the base object

        Args:
            id_ (str): The id of the Airtable base.
            key (str): The API key of the user that will connect the base.

            schema (str): The JSON filename describing the schema.

                To generate it, go to https://airtable.com/api and select a base. Then
                open your browsers console (Ctrl+Alt+I) and run the following:

                ```javascript
                var myapp = {
                    id:window.application.id,
                    name:window.application.name,
                    tables:[]
                };

                for (let table of window.application.tables){

                    var mytable = {
                            id:table.id,
                            isEmpty:table.isEmpty,
                            name:table.name,
                            nameForUrl:table.nameForUrl,
                            primaryColumnName:table.primaryColumnName,
                            fields:[]
                    };

                    for (let field of table.fields){
                        var myfield = {
                            id:field.id,
                            name:field.name,
                            type:field.type,
                            typeOptions:field.typeOptions
                        };

                        mytable.fields.push(myfield);

                    }

                    myapp.tables.push(mytable);

                }

                jQuery('link[rel=stylesheet]').remove();
                jQuery("body").html(JSON.stringify(myapp));
                console.log(myapp);
                ```

            renamer (TYPE, optional): Callable to transform table into class names.

                For instance, people may wanst to singularize the table names using the
                inflection package.
        """
        object.__init__(self)
        self._id = id_
        self._key = key
        with open(schema) as fle:
            self._schema = json.loads(fle.read())
            for table_schema in self._schema["tables"]:
                name = renamer(table_schema["name"])
                setattr(
                    self, Model.to_singularized_pascal_case(name), Model(table_schema)
                )

        @property
        def id(self):
            # pylint: disable=C0103,W0612,W0622
            """The base base_id.

            Returns:
                str: The base base_id.
            """
            return self._id

        @property
        def key(self):
            """The API key.

            Returns:
                str: The API key.
            """
            # pylint: disable=E0102
            return self._key

        @property
        def schema(self):
            """The shema dictionary.

            Returns:
                dict: The schema as a dictionary.
            """
            # pylint: disable=E0102
            return self._schema
