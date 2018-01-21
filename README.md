# Let's write: service registry

## Overview
This service is responsible of keeping track of services within the system.
It is a restful way for services to find other services, ensure that they are
healthy.

### Project requirements
Basic list of requirements can be foud in `featrues` directory that highlights
the very high overview of how it is supposed to be working. It is intentionally
left like that as details of implementation are left to you. Any changes
and decisions you make should be reflected in feature files with corresponding
steps implementation for [Behave](http://pythonhosted.org/behave/). In short if
it is not in feature files, it doesn't exist and has no right to exist in code.

## Running
This project was implemented using Python 3.6.1. For running it, ensure a
virtualenv with Python 3.6+ and install the requirements:

    $ pip install -r requirements.txt

Then set up the database (the default is a sqlite3 database):

    $ python manage.py migrate

Finally, run the server:

    $ python manage.py runserver

The API is now available at http://localhost:8000

## Tests
This project contains behavior and unit tests implemented. To run the unit
tests, ensure you install the test requirements:

    $ pip install -r requirements-test.txt

Then, for the unit tests:

    $ pytest api --cov api --cov-report term-missing

And for behavior tests:

    $ python manage.py behave
