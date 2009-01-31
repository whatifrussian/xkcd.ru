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

urlpatterns = patterns('',
# Example:
#     (r'^xkcd/', include('xkcd.apps.foo.urls.foo')),
# Uncomment this for admin:
url(r'^admin/(.*)', admin.site.root, name='admin-root'),
(r'^$', 'comics.views.last'),
(r'^num/$', 'comics.views.index_numbers'),
(r'^img/$', 'comics.views.index_thumbnail'),
(r'^(?P<comics_id>\d+)/$', 'comics.views.detail'),
(r'^(?P<comics_id>\d+)/(?P<timestamp>\d+)/$', 'comics.views.detail_unpublished'),
(r'^random/(?P<comics_id>\d+)/$', 'comics.views.random'),
(r'^random/$', 'comics.views.random'),
(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
#for users
(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'comics/login.html'}),
url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
(r'^unpublished/$', 'comics.views.index_unpublished'),
(r'^(?P<comics_id>\d+)/edit/$', 'comics.views.edit'),
(r'^add/$', 'comics.views.add'),
(r'^profile/$', 'profile.views.edit'),
(r'^(?P<comics_id>\d+)/livejournal/$', 'livejournal.views.post'),
(r'^(?P<comics_id>\d+)/transcript_form/$', 'transcript.views.show_form'),
(r'^(?P<comics_id>\d+)/transcript_save/$', 'transcript.views.add'),
(r'^(?P<comics_id>\d+)/transcript_thanks/$', 'transcript.views.thanks'),
(r'^(?P<comics_id>\d+)/transcript_edit/$', 'transcript.views.edit'),
(r'^(?P<comics_id>\d+)/transcript_clear/$', 'transcript.views.clear_unapproved'),
(r'^(?P<comics_id>\d+)/transcription/$', 'transcript.views.show_transcription'),
) + urlpatterns_local
