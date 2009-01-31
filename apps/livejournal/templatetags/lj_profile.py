import re

from django import template
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

from profile.models import Profile


register = template.Library()

lj_pattern = re.compile(r"^http://([-a-z0-9]+)\.livejournal\.com/?$")

@register.filter
def profile(value):
    try:
        profile = value.get_profile()
        m = lj_pattern.match(profile.url)
        if m:
            lj_user = m.group(1).replace('-', '_')
            if profile.nick:
                return mark_safe('%s (<lj user="%s">)' %
                                 (conditional_escape(profile.nick), lj_user))
            else:
                return mark_safe('<lj user="%s">' % lj_user)
        elif profile.url:
            return mark_safe('<a href="%s">%s</a>' %
                             (profile.url, conditional_escape(profile.nick )
                              if profile.nick else str(value) ))
        elif profile.nick:
            return profile.nick
    except Profile.DoesNotExist:
        pass
    # This is always safe?.
    return str(value)

profile.is_safe = True
