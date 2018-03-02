Accio: cli tool to manage AWS infrastructure for ML development
===============================================================

Accio definition: A charm that allows the caster to summon an object.

CLI Commands
------------

All CLI commands listed assume you have this alias set::

    alias accio="pipenv run python manage.py"

Examples
--------

I want to create a new stack named `mystack` with the default template::

    $ accio create-stack mystack
