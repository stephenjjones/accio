Accio: AWS GPU Resources for ML developers on a budget
======================================================

**Accio is a cli tool for managing AWS infrastructure.**

AWS p2 and p3 instances can be quite expensive for an independent ML developer. Creating new
resources, dyanimically changing ec2 instance types, starting/stopping instances, etc can be time
consuming and error prone.  Accio allows you to do all this in a few simple commands from your terminal.

.. image:: https://i.amz.mshcdn.com/ZjRzpcX1wS2o-py5V0aqR2RHiIA=/950x534/filters:quality(90)/2016%2F02%2F04%2F77%2FHarry_Potte.56329.jpg

**Accio:** A charm that allows the caster to summon an object.

Resources Description
---------------------

**Modify accio/templates/mystack to change attributes of the stack**

Defaults:

- ami: ami-66506c1c `ami reference <https://github.com/stephenjjones/accio/blob/master/ami.rst/>`_

  - ubuntu 16 LTS
  - nvidia docker (9.1)

- EBS backed ec2 instance
- EBS Volume has 100GB (gp2)
- VPC + subnet
- Internet Gateway 
- elasticIP
- Security Group

  - tcp 22 (ssh)
  - tcp 8888

Installation
------------

Accio is under rapid development and has not yet been published to PyPA.

Clone the Accio github repo::

    $ git clone git@github.com:stephenjjones/accio.git
    $ cd accio

Highly recommended to use pipenv to manage python environment and dependencies::

    $ pipenv install

All CLI commands listed assume you have the **accio** alias set, and that you run them from the
accio root directory::

    $ alias accio="pipenv run python accio/cli.py"
    # OR
    $ source alias.sh

Alternatively, you can pip install to get the accio cli available outside the project root::

    $ pip install .

Examples
--------

** All commands must be run from 

I want to create a new stack named `mystack` with the default template::

    $ accio create-stack mystack

I want to ssh into my new ec2 instance::

    $ accio ssh

I want to change my ec2 instance type to p3::

    $ accio update-stack

I want to stop a running instance::

    $ accio stop

I want to start a stopped instance::

    $ accio start

I want to delete my stack named `mystack`::

    $ accio delete-stack mystack

Uploads a local ssh key from ~/.ssh/[keyname] to the ec2 instance. **TODO: make .pem and id_rsa
keyname dynamic, currently hardcoded**::

    $ accio upload-keys



Misc Commands
-------------

Check cuda version::
  $ nvcc --version
