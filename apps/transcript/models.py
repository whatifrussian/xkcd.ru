# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ModelForm

from comics.models import Comics


class Transcription(models.Model):
    comics = models.OneToOneField(Comics, primary_key=True)

    transcription = models.TextField('Транскрипция')

    def __unicode__(self):
        return self.transcription[:10]+'...'

# There can be many unapproved transcriptions.
class UnapprovedTranscription(models.Model):
    comics = models.ForeignKey(Comics)

    transcription = models.TextField('Транскрипция')

    def __unicode__(self):
        return self.transcription[:10]+'...'

class TranscriptionForm(ModelForm):
    class Meta:
        model = Transcription
        exclude = ('comics')

class UnapprovedTranscriptionForm(ModelForm):
    class Meta:
        model = UnapprovedTranscription
        exclude = ('comics')
