# airstorm

[![PyPI version](https://badge.fury.io/py/airstorm.svg)](https://badge.fury.io/py/airstorm)
[![Documentation Status](https://readthedocs.org/projects/airstorm/badge/?version=latest)](https://airstorm.readthedocs.io/en/latest)
[![codecov](https://codecov.io/gh/douglaslassance/airstorm/branch/main/graph/badge.svg?token=5267NA3EQQ)](https://codecov.io/gh/douglaslassance/airstorm)

Airstorm is a dynamic Python ORM for [Airtable](https://airtable.com). It allows you to easily interact with any base using Python with minimal setup.

## Main Features

* Object-oriented interface.
* Dynamic generation of data models from schema.
* Automatic foreign-key resolution.
* Caching layer to avoid abusing the Airtable API.

## Installation

```bash
pip install airstorm
```

## Usage

```python
from airstorm.base import Base
jamba_juice = Base('your_base_id', 'your_api_key', {'your': 'schema'})
smoothy = jamba_juice.Smoothie('some_smoothie_id')  # Get your table record.
for fruit in smoothy.fruits:  # Get linked record in a breeze.
    print(fruit.name)  # Access any field data.
```

## Getting the Schema

Unfortunatly currently this part of the process is not ideal.
Because Airtable does not provide access to the schema via their API, you'll have to "download" the schema manually via a web browser of choice.

The following [gist](https://gist.github.com/douglaslassance/0ba26f2cf2aa9bb21a521ba07d751244) is a script that you can run on a Chrome console from the Airtable base [API page](https://airtable.com/api) to get back the JSON schema that airtstorm is expecting to be fed with.

## Roadmap

* Field validation where possible.
* Push changes. Currently we are read-only.
* Downlading schema automatically using pyppeteer.
* Advance queries. Lot to think about here.
