from django.db import models

from comics.models import Comics


class Post(models.Model):
    comics = models.ForeignKey(Comics, unique=True)

    url = models.CharField('URL', max_length=200)
    pid = models.IntegerField('Post id')
