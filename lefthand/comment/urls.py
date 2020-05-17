from django.urls import path

from .views import CommentView

app_name = 'comment'

urlpatterns = [
    path('comment/', CommentView.as_view(), name='comment'),
]
