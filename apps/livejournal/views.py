import sys

import lj

from django.conf import settings

from django.template import loader, Context
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test
from django.db import IntegrityError
from django.utils.encoding import iri_to_uri

from comics.models import Comics
from livejournal.models import Post
from profile.models import Profile


@user_passes_test(lambda u: u.is_staff)
def post(request, comics_id):
    comics_id = int(comics_id)
    comics = get_object_or_404(Comics, cid=comics_id, visible=True)
    try:
        lj_post = Post.objects.get(comics=comics)
    except Post.DoesNotExist:
        lj_post = None
    # Raise exception if we doesn't have this.
    settings.LJ_LOGIN
    settings.LJ_PASSWORD
    settings.LJ_JOURNAL
    try:
        lj_server = lj.rpcServer(settings.LJ_LOGIN, settings.LJ_PASSWORD,
                                 'xkcd.ru (contact dav03 at xkcd.ru)')
        t = loader.get_template('livejournal/code.html')
        c = {'comics': comics, 'user': comics.author}
        to_post = lj.Post(comics.title, str(t.render(Context(c))))
        time = comics.published.strftime(lj.LJ_TIME_FORMAT)
        if lj_post:
            result = lj_server.edit(lj_post.pid, time, to_post,
                                    settings.LJ_JOURNAL)
            return HttpResponseRedirect(comics.get_absolute_url() +
                                        '?lj=updated')
        else:
            result = lj_server.post(to_post, time, settings.LJ_JOURNAL,
                                    True)
            post = Post(comics=comics, url=result['url'],
                        pid=result['itemid'])
            post.save()
            return HttpResponseRedirect(comics.get_absolute_url() +
                                        '?lj=published')
    except Exception as e:
            return HttpResponseRedirect(comics.get_absolute_url() +
                                        iri_to_uri('?lj=error&msg=%s:%s' %
                                                   (sys.exc_info()[:2])))
