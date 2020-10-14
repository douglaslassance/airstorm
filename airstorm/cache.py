import logging

from airtable import Airtable
from requests.exceptions import HTTPError


class Cache(dict):
    """A cache object leaves on each object and is responsible for talking to Airtable
    and caching its data."""

    def __init__(self, base_id: str, api_key: str, table_id: str, index=False):
        """Initializes the cache object.

        Args:
            base_id (str): The base_id for this cache.
            api_key (str): The api_key for this cache.
            table_id (str): The table_id for this cache.
            index (bool, optional): Will index the enitire table on initialization.
        """
        dict.__init__(self)
        self._airtable = Airtable(base_id, table_id, api_key)
        if index:
            records = self._airtable.get_all()
            for record in records:
                self[record["id"]] = record

    def __getitem__(self, key):
        if not isinstance(key, str):
            return dict.__getitem__(self, key)
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            try:
                value = self._airtable.get(key)
            except HTTPError:
                logging.warning("Record {} was not found.".format(key))
                value = {}
            self.__setitem__(key, value)
        return dict.__getitem__(self, key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
