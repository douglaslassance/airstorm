# airstorm

[![codecov](https://codecov.io/gh/douglaslassance/airstorm/branch/main/graph/badge.svg?token=5267NA3EQQ)](undefined)
[![Documentation Status](https://readthedocs.org/projects/airstorm/badge/?version=latest)](https://airstorm.readthedocs.io/en/latest)

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
base = Base('your_base_id', 'your_api_key', {'your': 'schema'})
fruit_juice = base.FruitJuice('some_fruit_juice_id')  # Accessing the model for the "Fruit Juices" table.
price_tag = fruit_juice.price_tag  # Accessing the "Price Tag" field value.
for fruit in fruit_juice.fruits:  # Accessing a linked record in a breeze.
    print(fruit.name)
```

## Getting the Schema

Unfortunatly currently this part of the process is not ideal.
Because Airtable does not provide access to the schema via their API, you'll have to "download" the schema manually via a web browser of choice.

The following [gist](https://gist.github.com/douglaslassance/0ba26f2cf2aa9bb21a521ba07d751244) is a script that you can run on a Chrome console from the Airtable base [API page](https://airtable.com/api) to get back the JSON schema that airtstorm is expecting to be fed with.

## Roadmap

* Downlading schema automatically using pyppeteer.
* Field validation where possible.
* Auto-generated model lists.
* Push changes. Currently we are read-only.
* Advance queries. Lot to think about here.
