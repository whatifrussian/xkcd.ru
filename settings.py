import os
from settings_local import *

PROJECT_ROOT = os.path.dirname(__file__)

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

AUTH_PROFILE_MODULE = "profile.profile"

ROOT_URLCONF = 'urls'

# Yes, it's different specially. Django broke
# url rewriting in DEBUG mode if URL starts with
# STATIC_URL.
# Note: with external webserver /admin page will
# refer to files via /static/ (Django 1.6.5) or
# to /s/ (Django 1.6.3).
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")
STATIC_URL = '/s/'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'comics',
    'profile',
    'livejournal',
    'transcript',
    'statistics',
    'maillist'
)

WSGI_APPLICATION = "wsgi.application"
