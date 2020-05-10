from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post, Category, Tag
from config.models import SideBar

class CommonViewMixin:
    def get_context_date(self, **kwargs):
        context = super().get_context_date(**kwargs)
        context.update({
            'sidebars': SideBar.get_all()
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 7
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_date(self, **kwargs):
        context = super().get_context_date(**kwargs)
        category_pk = self.kwargs.get('category_pk')
        category = get_object_or_404(Category, pk=category_pk)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """ 重写 queryset，根据分类过滤 """
        queryset = super().get_queryset()
        category_pk = self.kwargs.get('category_pk')
        return queryset.filter(category_id=category_pk)


class TagView(IndexView):
    def get_context_date(self, **kwargs):
        context = super().get_context_date(**kwargs)
        tag_pk = self.kwargs.get('tag_pk')
        tag = get_object_or_404(Tag, pk=tag_pk)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """ 重写 queryset，根据标签过滤 """
        queryset = super().get_queryset()
        tag_pk = self.kwargs.get('tag_pk')
        return queryset.filter(tag_id=tag_pk)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    context_object_name = 'post'
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_pk'
