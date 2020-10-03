from setuptools import setup

setup(
    name='airstorm',
    version='0.1.0',  
    description='A Python ORM for Airtable.',
    url='https://github.com/playsthetic/airstorm',
    author='Douglas Lassance',
    author_email='douglassance@gmail.com',
    license='MIT',
    packages=['airstorm'],
    install_requires=[
        'airtable-python-wrapper==0.15.1',
    ],
    tests_requires=[
        'sphinx',
        'recommonmark'
        'sphinx-rtd-theme'
        'pytest',
        'pytest-pep8',
        'pytest-cov',
    ],
    include_package_data=True,
)