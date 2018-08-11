Installation
============

prerequisite:

- Python 3
- Python Virtual Environment
- MySQL database

Install Command:

- Activate your Python Virtual Environment
- Install project package requirement, run command:

::

    $ pip install -r requirement.txt

- Create database schema in your local mysql database
- Change orator connection in orator.yaml
- Create database table & data, run command:

::

    $ orator migrate --seed -c orator.yaml

Uninstall Command:

- Remove database table & data, run command:

::

    $ orator migrate:reset -c orator.yaml

- Remove project package requirement, run command:

::

    $ pip uninstall -r requirement.txt
