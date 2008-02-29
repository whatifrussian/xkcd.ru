from django.conf.urls.defaults import *
from comics.feeds import LatestComics

feeds = {
'xkcd': LatestComics,
}

urlpatterns = patterns('',
# Example:
#     (r'^xkcd/', include('xkcd.apps.foo.urls.foo')),
# Uncomment this for admin:
(r'^admin/comics/preview/(?P<comics_id>\d+)/$', 'comics.admin_views.preview'),
(r'^admin/comics/index_thumbnail/$', 'comics.admin_views.index_thumbnail'),
(r'^admin/', include('django.contrib.admin.urls')),
(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/davidov/my/misc/media/media'}),
(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/davidov/my/misc/media/static'}),
(r'^xkcd_img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/davidov/my/misc/media/xkcd_img'}),
(r'^xkcd_thumb/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/davidov/my/misc/media/xkcd_thumb'}),
(r'^xkcd/$', 'comics.views.index'),
(r'^xkcd/img/$', 'comics.views.index_thumbnail'),
(r'^xkcd/(?P<comics_id>\d+)/$', 'comics.views.detail'),
(r'^xkcd/(?P<comics_id>\d+)/(?P<timestamp>\d+)/$', 'comics.views.detail_unpublished'),
(r'^xkcd/random/(?P<comics_id>\d+)/$', 'comics.views.random'),
(r'^xkcd/random/$', 'comics.views.random'),
#(r'^xkcd/(?P<comics_id>\d+)/code/$', 'comics.views.code'),
(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
#for users
(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'comics/login.html'}),
url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/xkcd/'}, name='logout'),
(r'^xkcd/unpublished/$', 'comics.views.index_unpublished'),
(r'^xkcd/(?P<comics_id>\d+)/edit/$', 'comics.views.edit'),
(r'^xkcd/add/$', 'comics.views.add'),
)


