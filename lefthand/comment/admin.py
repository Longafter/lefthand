from django.contrib import admin

from .models import Comment

from lefthand.custom_site import custom_site


@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_play = ('target', 'nickname', 'content', 'website', 'created_time')
