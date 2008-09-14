from django.conf.urls.defaults import *
from django.contrib import admin
from comics.feeds import LatestComics
import specific.urls

admin.autodiscover()

feeds = {
'xkcd': LatestComics,
}

urlpatterns = patterns('',
# Example:
#     (r'^xkcd/', include('xkcd.apps.foo.urls.foo')),
# Uncomment this for admin:
(r'^admin/(.*)', admin.site.root),
(r'^$', 'comics.views.index'),
(r'^img/$', 'comics.views.index_thumbnail'),
(r'^(?P<comics_id>\d+)/$', 'comics.views.detail'),
(r'^(?P<comics_id>\d+)/(?P<timestamp>\d+)/$', 'comics.views.detail_unpublished'),
(r'^random/(?P<comics_id>\d+)/$', 'comics.views.random'),
(r'^random/$', 'comics.views.random'),
(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
#for users
(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'comics/login.html'}),
url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/xkcd/'}, name='logout'),
(r'^unpublished/$', 'comics.views.index_unpublished'),
(r'^(?P<comics_id>\d+)/edit/$', 'comics.views.edit'),
(r'^add/$', 'comics.views.add'),
)+specific.urls.urlpatterns
