from django.db import models

from comics.models import Comics


class Post(models.Model):
    comics = models.ForeignKey(Comics, unique=True)

    url = models.URLField('URL',verify_exists=False)
    pid = models.IntegerField('Post id')
