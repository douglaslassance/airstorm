import os



class Base(object):
	"""The base class is the root object to access the airtable base.
	"""

	def __init__(self, base_id, api_key, schema_filename):
		"""Intialize the base object
		
		Args:
		    base_id (TYPE): The id of the Airtable base.
		    api_key (TYPE): The API key of the user that will connect the base.

		    schema_filename (TYPE): The JSON file describing the schema Visit.

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
							columns:[]
					};

					for (let column of table.columns){
						var mycolumn = {
							id:column.id,
							name:column.name,
							type:column.type,
							typeOptions:column.typeOptions
						};

						mytable.columns.push(mycolumn);

					}

					myapp.tables.push(mytable);

				}

				jQuery('link[rel=stylesheet]').remove();
				jQuery("body").html(JSON.stringify(myapp));
				console.log(myapp);
				```
		"""
		super(Base, self).__init__()
		self._base_id = base_id
		self._api_key = api_key
		with open(os.environ.get('AIRSTORM_SCHEMA')) as fle:
			self._schema = json.loads(fle.read())

		@property
		def base_id(self):
			"""The base id.
			
			Returns:
			    str: The base id.
			"""
			return self._base_id

		@property
		def api_key(self):
			"""The API key.
			
			Returns:
			    str: The API key.
			"""
			return self._api_key

		@property
		def schema(self):
			"""The shema dictionary.
			
			Returns:
			    dict: The schema as a dictionary.
			"""
			return self._schema
		

		