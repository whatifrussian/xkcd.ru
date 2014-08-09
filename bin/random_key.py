#!/usr/bin/env python

# http://stackoverflow.com/questions/4664724/distributing-django-projects-with-unique-secret-keys/16630719#16630719

from django.utils.crypto import get_random_string

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
key = get_random_string(50, chars)
print ("SECRET_KEY = '" + key + "'")
