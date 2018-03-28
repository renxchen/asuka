"""
Django settings for newwebday2 project.

Generated by 'django-admin startproject' using Django 1.9.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$x=wa!v!@^lm48y9lol)#91-c42-x&ths!z*s7agl3^mt0=5%y'
# SECRET_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidXNlcl9pZCI6MSwiZW1haWwiOiJraW1saUBjaXNjby5jb20iLCJleHAiOjE1MTE1MDY5NTh9.3a3It7YVQn4mCJjd7cljCbaLHWy8TmbFq9qKmEbP85Q'

# SECURITY WARNING: don't run with debug turned on in production!
#
INSTALLED_APPS = [
    'backend.apolo'
]

from backend.server.settings import DATABASES as db

DATABASES = db
