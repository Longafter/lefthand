from django.urls import path

from .views import (
    IndexView, CategoryView, TagView,
    PostDetailView,
)

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<int:category_pk>/', CategoryView.as_view(), name='post-category'),
    path('tag/<int:tag_pk>/', TagView.as_view(), name='post-tag'),
    path('post/<int:post_pk>/', PostDetailView.as_view(), name='post-detail'),
]
