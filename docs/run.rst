Run the project
===============

- change project mysql connection in config.cfg
- python run.py

**Website**

- url: http://127.0.0.1:8899/
- username: admin, password: 123456

**Restful Api**

Login:

- api url: POST http://127.0.0.1:8899/api/v1/user/login
- header: 

::

    Content-Type:application/json

- request parameter: 

::

    { 
        "username" : "admin", 
        "password" : "123456" 
    }

User List:

- api url: POST http://127.0.0.1:8899/api/v1/user/list
- header: 

::

    Authorization:Bearer <jwt_token> 
    Content-Type:application/json

- request parameter: 

::

    { 
        "rp" : <RecordPerPage>, 
        "p" : <Page>, 
        "f" : {
            "<field_name>":"<field_value>"
        },
        "q" : "<raw_query>"
        "o" : {"<field_name>":"<asc_desc>"},
    }

Import file **albasia.postman_collection** to your postman to try the restful api.