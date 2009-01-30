from django.contrib import admin

from comics.models import Comics
from livejournal.models import Post


class PostInline(admin.StackedInline):
	model = Post

class ComicsAdmin(admin.ModelAdmin):
        list_display = ('cid', 'title', 'image_preview', 'visible')
        ordering = ('visible', )
        list_per_page = 10

	inlines = [PostInline]


admin.site.register(Comics, ComicsAdmin)
