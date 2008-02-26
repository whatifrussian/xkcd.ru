from django.db import models
from django.db.models import permalink


# Create your models here.
class Comics(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(maxlength=255)
    image = models.ImageField(upload_to='xkcd_img/')
    thumbnail = models.ImageField(upload_to='xkcd_thumb/')
    text = models.TextField()
    visible = models.BooleanField()
    comment = models.TextField(blank=True)
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    updated = models.DateTimeField('date updated', auto_now=True)
    
    #def __unicode__(self):
    #    return self.title
    def __str__(self):
        return "%s: %s" % (self.id, self.title)
    
    #def image_view(self):
    #    return "<img src='%s' alt=''/>" % (self.get_image_url())

    #image_view.allow_tags = True
    def get_absolute_url(self):
        if self.visible: 
            return ('comics.views.detail', [str(self.id)])
        else:
            return ('comics.views.detail_unpublished', [str(self.id), self.pub_date.strftime('%s')])

    get_absolute_url = permalink(get_absolute_url)

    def image_preview(self):
        return '<a href="%s" title="%d: %s"><img border=0 src="%s" alt="%s"></a>' % (self.get_absolute_url(), self.id, self.title, self.get_thumbnail_url(), self.title)

    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'

    class Admin:
	#fields = (
        #    (None, {'fields': ('id', 'title', 'image', 'text', 'comment', 'image_preview')}),
        #)
        list_display = ('id', 'title', 'image_preview', 'visible')
        #list_display = ('id', 'title', 'visible')
        ordering = ('visible', )
        list_per_page = 10
        #pass
