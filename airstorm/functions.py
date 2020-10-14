"""This module hosts a handfull fo re-usable functions.
"""

import inflection


def to_singular_pascal_case(name: str):
    """Make any name into a valid singulatized PascalCased name.

    Args:
        name (TYPE): The name to singularized PascalCase.

    Returns:
        str: The singularized PascalCased name.
    """
    return inflection.singularize(
        inflection.camelize(
            inflection.parameterize(inflection.titleize(name), separator="_")
        )
    )


def to_snake_case(name: str):
    """Make any name into a valid snake_cased name.

    Args:
        name (str): The name to snake_case.

    Returns:
        TYPE: The snake_cased name.
    """
    return inflection.parameterize(inflection.titleize(name), separator="_").lower()
