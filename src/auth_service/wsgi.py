"""
WSGI config for auth_service project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from typing import Union

from django.core.wsgi import get_wsgi_application

# Collect the current environment (development | production)
environment: Union[str, None] = os.environ.get("ENV")

# Check for specified enviornment and set settings file location
if environment.lower() == "development":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
elif environment.lower() == "production":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
else:
    raise EnvironmentError("Could not detect environment from .env file.")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')

application = get_wsgi_application()
