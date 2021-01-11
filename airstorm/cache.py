import logging

from airtable import Airtable
from requests.exceptions import HTTPError


class Cache(dict):
    """A cache instance live on each model and is used by other classes to access
    the Airtable data. The cache object automatically get stuff it does not have
    available locally when requested

    Args:
        base_id (str): The base_id for this cache.
        api_key (str): The api_key for this cache.
        table_id (str): The table_id for this cache.
        indexed (bool, optional): Will index the enitire table on initialization.
    """

    def __init__(self, model):

        dict.__init__(self)
        self._model = model
        self._airtable = Airtable(
            self._model._base._id, model._id, self._model._base._api_key
        )
        if model._indexed:
            self._model._base._hits += 1
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
                self._model._base._hits += 1
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

    def select(self, formula=""):
        """Select multiple records in Airtable matching the provided formula.

        Args: formula (str, optional): A airtable formula to filter the search. Lean
            more about writing valid formulas at
            https://support.airtable.com/hc/en-us/articles/203255215-Formula-Field-Reference.

        Returns:
            dict: The data selected.
        """

        # TODO: Needs to take indexing into account when a formula is passed.
        # Currently will always hit Airtable.
        if not formula and self._model._indexed:
            return self

        kwargs = {}
        if formula:
            kwargs["formula"] = formula
        self._model._base._hits += 1
        records = self._airtable.get_all(**kwargs)
        cache = {}
        for record in records:
            id_ = record["id"]
            cache[id_] = record
        self.update(cache)
        return cache
