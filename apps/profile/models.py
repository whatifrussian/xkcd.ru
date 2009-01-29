# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)

    url = models.URLField('URL', verify_exists=False, blank=True)
    town = models.CharField('Город', max_length=100, blank=True)

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user')
