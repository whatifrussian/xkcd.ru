from django.contrib import admin

from comics.models import Comics
from livejournal.models import Post
from transcript.models import UnapprovedTranscription, Transcription


class PostInline(admin.StackedInline):
	model = Post

class UnapprovedTranscriptionInline(admin.StackedInline):
	model = UnapprovedTranscription

class TranscriptionInline(admin.StackedInline):
	model = Transcription

class ComicsAdmin(admin.ModelAdmin):
        list_display = ('cid', 'title', 'image_preview', 'visible', 'author')
        ordering = ('visible', )
        list_per_page = 10

	inlines = [PostInline, TranscriptionInline,
		   UnapprovedTranscriptionInline]



admin.site.register(Comics, ComicsAdmin)
