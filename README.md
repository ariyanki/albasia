# albasia
Python Flask MVC Project Template

pre requisite:
- Python 3
- Python Virtual Environment
- mysql database

Install Command:
- pip install -r requirement.txt
- create mysql database schema
- change orator connection in orator.yaml
- orator migrate --seed -c orator.yaml

Uninstall Command:
- orator migrate:reset -c orator.yaml
- pip uninstall -r requirement.txt

Run:
- change project mysql connection in config.cfg
- python run.py
- url: http://127.0.0.1:8899/
- username: sadmin, password: 123456
- api url: POST http://127.0.0.1:8899/api/v1/user/login
- header: Content-Type:application/json
- request parameter: { "username":"sadmin", "password":"123456" }


See the documentation [http://albasia.readthedocs.org](http://albasia.readthedocs.org)
