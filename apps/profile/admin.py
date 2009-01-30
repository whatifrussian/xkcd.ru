from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from profile.models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile

class MyUserAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
