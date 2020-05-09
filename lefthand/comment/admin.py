from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_play = ('target', 'nickname', 'content', 'website', 'created_time')
