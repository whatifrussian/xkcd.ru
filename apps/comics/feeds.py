# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed

from comics.models import Comics


class LatestComics(Feed):
    title = "xkcd по-русски"
    link = "/"
    description = "Новые переводы комиксов xkcd на русский язык."
    
    def items(self):
        return Comics.objects.filter(visible = True)\
            .order_by('-published')[:10]

    def item_pubdate(self, item):
        return item.published

    def item_author_name(self, item):
        return item.author
