import xadmin

from .models import Comment


@xadmin.sites.register(Comment)
class CommentAdmin:
    list_play = ('target', 'nickname', 'content', 'website', 'created_time')
