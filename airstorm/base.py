"""Module holding the base class definition.
"""

import json

from .model import Model


class Base:
    # pylint: disable=R0903
    """The base class is the root object to access the airtable base."""

    def __init__(self, id_, api_key, schema, renamer=lambda x: x):
        """Intialize the base object

        Args:
            id_ (str): The id of the Airtable base.
            api_key (str): The API key of the user that will connect the base.

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
        self._api_key = api_key
        with open(schema) as fle:
            self._schema = json.loads(fle.read())
            for table_schema in self._schema["tables"]:
                name = renamer(table_schema["name"])
                class_name = Model.to_singular_pascal_case(name)
                class_dict = {
                    "_schema": table_schema,
                    "_base": self,
                }
                setattr(self, class_name, Model(class_name, (), class_dict))

        @property
        def id(self):
            # pylint: disable=invalid-name, redefined-builtin, unused-variable
            """The base base_id.

            Returns:
                str: The base base_id.
            """
            return self._id

        @property
        def api_key(self):
            """The API key.

            Returns:
                str: The API key.
            """
            # pylint: disable=function-redefined
            return self._api_key

        @property
        def schema(self):
            """The shema dictionary.

            Returns:
                dict: The schema as a dictionary.
            """
            # pylint: disable=function-redefined
            return self._schema
