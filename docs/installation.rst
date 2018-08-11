Installation
============

pre requisite:

- Python 3
- Python Virtual Environment
- MySQL database

Install Command:

- Activate your Python Virtual Environment
- pip install -r requirement.txt
- create database schema in your local mysql database
- change orator connection in orator.yaml
- orator migrate --seed -c orator.yaml

Uninstall Command:

- orator migrate:reset -c orator.yaml
- pip uninstall -r requirement.txt
