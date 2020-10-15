"""This module holds general purpose functions.
"""

import inflection


def to_singular_pascal_case(name: str):
    """Make any string into a singular "PascalCased" string.

    Args:
        name (str): The string to convert.

    Returns:
        str: The converted string.
    """
    return inflection.singularize(
        inflection.camelize(
            inflection.parameterize(inflection.titleize(name), separator="_")
        )
    )


def to_snake_case(name: str):
    """Make any string into a "snake_cased" string.

    Args:
        name (str): The name to convert.

    Returns:
        str: The converted string.
    """
    return inflection.parameterize(inflection.titleize(name), separator="_").lower()
