from django.contrib.sitemaps import Sitemap

from comics.models import Comics


class ComicsSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5
    
    def items(self):
        return Comics.objects.filter(visible=True)

    def lastmod(self, obj):
        return obj.updated

