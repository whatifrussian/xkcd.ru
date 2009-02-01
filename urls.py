from django.conf.urls.defaults import *
from django.contrib import admin
from comics.feeds import LatestComics
try:
    from urls_local import urlpatterns as urlpatterns_local
except ImportError:
    urlpatterns_local = patterns('')

admin.autodiscover()

feeds = {
'xkcd': LatestComics,
}

urlpatterns = patterns(
    '',
    url(r'^admin/(.*)',
        admin.site.root, name='admin-root'),
    (r'^$', 'comics.views.last'),
    (r'^num/$', 'comics.views.index_numbers'),
    (r'^img/$', 'comics.views.index_thumbnail'),
    (r'^(?P<comics_id>\d+)/$', 'comics.views.detail'),
    (r'^(?P<comics_id>\d+)/(?P<timestamp>\d+)/$',
     'comics.views.detail_unpublished'),
    (r'^random/(?P<comics_id>\d+)/$', 'comics.views.random'),
    (r'^random/$', 'comics.views.random'),
    (r'^feeds/(?P<url>.*)/$',
     'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    # For users.
    (r'^login/$',
     'django.contrib.auth.views.login',
     {'template_name': 'comics/login.html'}),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
    (r'^unpublished/$',
     'comics.views.index_unpublished'),
    (r'^edit/(?P<comics_id>\d+)/$',
     'comics.views.edit'),
    (r'^add/$',
     'comics.views.add'),
    (r'^profile/$',
     'profile.views.edit'),
    (r'^livejournal/(?P<comics_id>\d+)/$', 'livejournal.views.post'),
    # Transcriptions.
    (r'^transcript_form/(?P<comics_id>\d+)/$', 'transcript.views.show_form'),
    (r'^transcript_save/(?P<comics_id>\d+)/$', 'transcript.views.add'),
    (r'^transcript_thanks/(?P<comics_id>\d+)/$', 'transcript.views.thanks'),
    (r'^transcript_edit/(?P<comics_id>\d+)/$', 'transcript.views.edit'),
    (r'^transcript_clear/(?P<comics_id>\d+)/$',
     'transcript.views.clear_unapproved'),
    (r'^transcription/(?P<comics_id>\d+)/$',
     'transcript.views.show_transcription'),
    (r'^unapproved/$', 'transcript.views.list_unapproved'),
    ) + urlpatterns_local
