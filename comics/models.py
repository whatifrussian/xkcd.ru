# *- coding: utf-8 *-
from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.newforms import ModelForm

# Create your models here.
class Comics(models.Model):
    cid = models.IntegerField("Номер", unique=True)
    title = models.CharField("Название", max_length=255)
    image = models.ImageField("Изображение",upload_to='xkcd_img/')
    thumbnail = models.ImageField("Миниатюра", upload_to='xkcd_thumb/')
    text = models.TextField("Подпись")
    comment = models.TextField("Комментарий", blank=True)
    visible = models.BooleanField("Виден", default=False)
    pub_date = models.DateTimeField('Опубликованно',auto_now_add=True)
    updated = models.DateTimeField('Обновлено', auto_now=True)
    author = models.ForeignKey(User)
    
    def __unicode__(self):
        return "%s: %s" % (self.cid, self.title)
    
	@permalink
    def get_absolute_url(self):
        if self.visible: 
            return ('comics.views.detail', [str(self.cid)])
        else:
            return ('comics.views.detail_unpublished', [str(self.cid), self.pub_date.strftime('%s')])

    def image_preview(self):
        return '<a href="%s" title="%d: %s"><img border=0 src="%s" alt="%s"></a>' % (self.get_absolute_url(), self.cid, self.title, self.get_thumbnail_url(), self.title)

    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'

    class Admin:
        list_display = ('cid', 'title', 'image_preview', 'visible')
        ordering = ('visible', )
        list_per_page = 10

class ComicsForm(ModelForm):
    class Meta:
        model = Comics
        exclude = ('pub_date', 'updated', 'visible', 'author')
