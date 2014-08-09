# -*- coding: utf-8 -*-

import re

from django import template
from django.utils.safestring import mark_safe, SafeData
from django.utils.html import conditional_escape

# This comes from django.
simple_email_re = re.compile(r'([^; \t\n\r\f\v])[^; \t\n\r\f\v]*@([a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+)')

register = template.Library()

@register.filter
def format_mail(value, autoescape=None):
    result = ""
    if autoescape:
        value = conditional_escape(value)
    value = simple_email_re.sub('\\1…@\\2', value)
    value = value.split('\n-- \n')[0]
    value = value.strip()
    for line in value.split('\n'):

        if line and line.startswith('&gt;'):
            result += '<cite>%s </cite><br/>' % line
        else:
            result += '%s <br/>\n' % line
    return mark_safe(result)
format_mail.needs_autoescape = True



