from django.conf.urls.defaults import *
from comics.feeds import LatestComics
import specific.urls

feeds = {
'xkcd': LatestComics,
}

urlpatterns = patterns('',
# Example:
#     (r'^xkcd/', include('xkcd.apps.foo.urls.foo')),
# Uncomment this for admin:
(r'^admin/', include('django.contrib.admin.urls')),
(r'^xkcd/$', 'comics.views.index'),
(r'^xkcd/img/$', 'comics.views.index_thumbnail'),
(r'^xkcd/(?P<comics_id>\d+)/$', 'comics.views.detail'),
(r'^xkcd/(?P<comics_id>\d+)/(?P<timestamp>\d+)/$', 'comics.views.detail_unpublished'),
(r'^xkcd/random/(?P<comics_id>\d+)/$', 'comics.views.random'),
(r'^xkcd/random/$', 'comics.views.random'),
(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
#for users
(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'comics/login.html'}),
url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/xkcd/'}, name='logout'),
(r'^xkcd/unpublished/$', 'comics.views.index_unpublished'),
(r'^xkcd/(?P<comics_id>\d+)/edit/$', 'comics.views.edit'),
(r'^xkcd/add/$', 'comics.views.add'),
)+specific.urls.urlpatterns
