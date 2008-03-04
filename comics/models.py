# *- coding: utf-8 *-
from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django import newforms as forms
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image
from cStringIO import StringIO
from django.newforms.fields import UploadedFile
from os.path import basename

# Create your models here.
class Comics(models.Model):
    cid = models.IntegerField("Номер", unique=True)
    title = models.CharField("Название", max_length=255)
    image = models.ImageField("Изображение", upload_to='xkcd_img/')
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

class ComicsForm(forms.ModelForm):
    preview_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    
    class Meta:
        model = Comics
        exclude = ('pub_date', 'updated', 'visible', 'author')

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data['thumbnail']
        try:
            image = Image.open(StringIO(thumbnail.content))
            if image.size != (48, 48):
                raise forms.ValidationError(u'Должно быть 48x48.')
            return thumbnail
        # This means that image is string.
        except AttributeError:
            return thumbnail

    def get_preview(self):
        try:
            return Preview.objects.get(id=self.data['preview_id'])
        except AttributeError:
            raise ObjectDoesNotExist()

    def create_preview(self):
        try:
            preview = self.get_preview()
        except ObjectDoesNotExist:
            preview = Preview()
        
        preview.set_images(self.cleaned_data['image'],
                           self.cleaned_data['thumbnail'])

        preview.save()
        
        self.data['preview_id'] = preview.id
        
        return preview


    def save(self, commit=True):
        this = forms.ModelForm.save(self, False)
        this.image = self.cleaned_data['image']
        this.thumbnail = self.cleaned_data['thumbnail']
        if commit:
            this.save()
        return this

class Preview(models.Model):
    image = models.ImageField("Изображение", upload_to='xkcd_img/')
    thumbnail = models.ImageField("Миниатюра", upload_to='xkcd_thumb/')
    pub_date = models.DateTimeField('Создано',auto_now_add=True)


    def set_images(self, image, thumbnail):

        if isinstance(image, UploadedFile):
            self.save_image_file(image.filename, image.content)
        else:
            self.image = image

        if isinstance(thumbnail, UploadedFile):
            self.save_thumbnail_file(thumbnail.filename, thumbnail.content)
        else:
            self.thumbnail = thumbnail
                    

    class Admin:
        pass

