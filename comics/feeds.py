from django.contrib.syndication.feeds import Feed
from comics.models import Comics

class LatestComics(Feed):
    title = "New on ru_xkcd"
    link = "/"
    description = "Updates on ru_xkcd archive."
    
    def items(self):
        return Comics.objects.filter(visible=True).order_by('-published')[:10]

    def item_pubdate(self,item):
        return item.published
