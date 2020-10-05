from setuptools import setup

setup(
    name="airstorm",
    version="0.1.0",
    description="A Python ORM for Airtable.",
    url="https://github.com/playsthetic/airstorm",
    author="Douglas Lassance",
    author_email="douglassance@gmail.com",
    license="MIT",
    packages=["airstorm"],
    install_requires=[
        # Generally accepting all minor version in a major. Making assumption that
        # people do their due diligence by not releasing breaking changes without
        # incrementing the major version.
        "airtable-python-wrapper>=0,<1",
        "inflection>=0,<1",
    ],
    extras_require={
        "ci": [
            "sphinx",
            "recommonmark",
            "sphinx-rtd-theme",
            "pytest",
            "pytest-pep8",
            "pytest-cov",
            "pytest-html",
            "flake8",
        ],
    },
    include_package_data=True,
)
