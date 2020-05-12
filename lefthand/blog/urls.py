from django.urls import path

from .views import (
    IndexView, CategoryView, TagView,
    SearchView, AuthorView, PostDetailView,
)

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='post-category'),
    path('tag/<int:tag_id>/', TagView.as_view(), name='post-tag'),
    path('search/', SearchView.as_view(), name='search'),
    path('owner/<int:owner_id>/', AuthorView.as_view(), name='owner'),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
]
