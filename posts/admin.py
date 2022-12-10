from django.contrib import admin

from posts.models import Posts

# Register your models here.

@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'profile', 'title', 'photo')
    list_display_links = ('pk', 'user')
    list_editable = ('profile', 'title', 'photo')
