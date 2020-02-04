# albasia
Python Flask MVC Project Template

See the documentation [http://albasia.readthedocs.org](http://albasia.readthedocs.org)

## Installation

pre requisite:
- Python 3
- Python Virtual Environment
- MySQL database
- MongoDB
- Redis

Install Command:
- Activate your Python Virtual Environment
- pip install -r requirement.txt
- create mysql database schema
- change orator connection in orator.yaml
- orator migrate --seed -c orator.yaml
- create folder app/resources/logs

Uninstall Command:
- orator migrate:reset -c orator.yaml
- pip uninstall -r requirement.txt

## Run

- change project mysql connection in config.cfg
- python run.py

## Testing
- py.test --maxfail=1 --cov=app -p no:warnings --cov-report xml:app/resources/coverage/test.xml tests/

### Website
- url: http://127.0.0.1:8899/
- username: admin, password: 123456

### Restful Api

Login:
- api url: POST http://127.0.0.1:8899/api/v1/user/login
- header: Content-Type:application/json
- request parameter: { "username":"admin", "password":"123456" }

User List:
- api url: POST http://127.0.0.1:8899/api/v1/user/list
- header: 
Authorization:Bearer <jwt_token>
Content-Type:application/json
- request parameter: 
{ 
	"rp":<RecordPerPage>, 
	"p":<Page>, 
	"f":{"<field_name>":"<field_value"},
	"o":{"<field_name>":"<asc_desc>"},
}

Import file **albasia.postman_collection** to your postman to try the restful api.


## Linux Service Configuration

This example is using gunicorn, Read about gunicorn [here](https://gunicorn.org)

Create Socket File:

```go
sudo nano /etc/systemd/system/albasia.socket
```

Socket File Content:
```go
[Unit]
Description=albasia socket

[Socket]
ListenStream=/tmp/albasia.sock

[Install]
WantedBy=sockets.target
```

Create Service File:
```go
sudo nano /etc/systemd/system/albasia.service 
```

Service File Content:
```go
[Unit]
Description=albasia daemon
Requires=albasia.socket
After=network.target

[Service]
PIDFile=/run/gunicorn/pid
User=root
Group=root
RuntimeDirectory=gunicorn
WorkingDirectory=/www/albasiabackend
ExecStart=export FLASK_ENV=production
ExecStart=/www/python37/bin/gunicorn --bind unix:/tmp/albasia.sock wsgi:app --timeout=30
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

notes: change directory path based on you configuration.

Start the socket:
```go
sudo systemctl start albasia.socket
sudo systemctl enable albasia.socket
```

Start the service:
```go
sudo systemctl start albasia.service
sudo systemctl enable albasia.service
```

## Nginx configuration

Add server configuration in your nginx site:
```go
server {
        listen          80;
        server_name     albasia.abcdef.id;
        location / {
            proxy_pass http://unix:/tmp/albasia.sock;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_set_header X-NginX-Proxy true;

            proxy_headers_hash_max_size 51200;
            proxy_headers_hash_bucket_size 6400;

            proxy_redirect off;
            proxy_connect_timeout       300;
            proxy_send_timeout          300;
            proxy_read_timeout          300;

            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

}
```

Restart nginx.


