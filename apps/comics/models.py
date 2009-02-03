# *- coding: utf-8 *-
from PIL import Image
from cStringIO import StringIO

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError


class Comics(models.Model):
    cid = models.IntegerField("Номер", unique=True)
    title = models.CharField("Название", max_length=255)
    image = models.ImageField("Изображение", upload_to='xkcd_img/')
    thumbnail = models.ImageField("Миниатюра", upload_to='xkcd_thumb/')
    text = models.TextField("Подпись")
    comment = models.TextField("Комментарий", blank=True)
    transcription = models.TextField("Транскрипция", blank=True)
    visible = models.BooleanField("Виден", default=False)
    created = models.DateTimeField('Создано', auto_now_add=True)
    published = models.DateTimeField('Опубликованно', null=True)
    updated = models.DateTimeField('Обновлено', auto_now=True)
    author = models.ForeignKey(User)
    
    def __unicode__(self):
        return "%s: %s" % (self.cid, self.title)
    
    @permalink
    def get_absolute_url(self):
        if self.visible: 
            return ('comics.views.detail', [str(self.cid)])
        else:
            return ('comics.views.detail_unpublished',
                    [str(self.cid), self.created.strftime('%s')])

    def image_preview(self):
        return '<a href="%s" title="%d: %s"><img border=0 src="%s" alt="%s">\
                    </a>' % (self.get_absolute_url(), self.cid, self.title,
                              self.thumbnail.url, self.title)

    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'


class ComicsForm(ModelForm):
    class Meta:
        model = Comics
        exclude = ('created', 'published', 'updated', 'visible', 'author')
    def clean_thumbnail(self):
       thumbnail = self.cleaned_data['thumbnail']
       try:
           image = Image.open(StringIO(thumbnail.read()))
           if image.size != (48, 48):
               raise ValidationError(u'Должно быть 48x48.')
           return thumbnail
       # This means that image is string.
       except AttributeError:
           return

class TranscriptionForm(ModelForm):
    class Meta:
        model = Comics
        fields = ('transcription',)
