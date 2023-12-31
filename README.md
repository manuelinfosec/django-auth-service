## About
Single service for user management and authentication within a microservice architecture; powered by Django Rest Framework (DRF).

### Installation/Serving
For local development next steps should be made:

```shell
virtualenv .venv --python=python3
source .venv/bin/activate
pip install -r requirements.txt
gunicorn auth_service.wsgi:application --bind 127.0.0.1:8000
# or
#   python manage.py runserver
```

For production usage, use:
```shell
docker build -t authservice .
docker run authservice     # No ports expose due to use of UNIX sockets
```

### Usage
Following endpoints are available:
```
register/ - Register new user
login/ - User login and retrieving JWT tokens
user/ - Manage user's account (GET/Update/DELETE)
protected/ - Test JWT Authentication and Authorization
token_verify/ - Verify JWT from external service
token_refresh/ - Refresh expired token
```

### Technologies 
```
Python3.7+
Django==3.2.15
djangorestframework==3.14.0
drf-jwt==1.19.1
```

### Documentation
Swagger API and Postman Collectio is available within the project.
Visit root URL for accessing Swagger.
![swagger screenshot](docs/swagger.png)

### Tests & Code Coverage
```shell
cd src
coverage run --source='.' manage.py test
coverage report
```