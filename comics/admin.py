from django.contrib import admin

from comics.models import Comics


class ComicsAdmin(admin.ModelAdmin):
        list_display = ('cid', 'title', 'image_preview', 'visible')
        ordering = ('visible', )
        list_per_page = 10


admin.site.register(Comics, ComicsAdmin)
