# -*- coding: utf-8 -*-

import re

from django.db import models

from comics.models import Comics


sender_re = re.compile('(.*) <([^<>]*)@([^<>]*)>')

class Mail(models.Model):
    sender = models.CharField(max_length=255)
    message = models.TextField()
    date = models.DateTimeField()
    comics = models.ForeignKey(Comics)
    
    def safe_sender(self):
        m = sender_re.match(self.sender)
        if m:
            return '%s <%s…@%s>' % (m.group(1), m.group(2)[0], m.group(3))
