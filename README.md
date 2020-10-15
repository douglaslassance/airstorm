# airstorm

Airstorm is a dynamic Python ORM for [Airtable](https://airtable.com). It allows you to easily interact with any base using Python with minimal setup.

## Main Features

* Object-oriented interface.
* Dynamic loading of data models.
* Automatic foreign-key resolution.
* Caching layer to avoid abusing the Airtable API.

## Installation

```bash
pip install airstorm
```

## Usage

```python
from airstorm import Base
base = Base('your_base_id', 'your_api_key', {'your_schema': ''})
fruit_juice = base.FruitJuice('some_fruit_juice_id')  # Accessing the model for the "Fruit Juices" table.
price_tag = fruit_juice.price_tag  # Accessing the "Price Tag" field value.
for fruit in fruit_juice.fruits:  # Accessing a linked record in a breeze.
    print(fruit.name)
```

## Getting the Schema

Unfortunatly currently this part of the process is not ideal.

## Roadmap

* Dynamic schema loading when Airtable finally upgrade their API.