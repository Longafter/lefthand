from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav', 'owner')

    # 将 owner 字段设定为当前的登录用户
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    # 显示分类下的文章数量
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = "文章数量"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status', 'owner')

    # 将 owner 字段设定为当前的登录用户
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator',
    ]
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
        'created_time',
    )
    # 配置哪些字段可以作为链接
    list_display_links = []
    # 配置页面过滤器，需要通过哪些字段来过滤列表页
    list_filter = ['category', ]
    # 配置搜索字段 
    search_fields = ['title', 'category__name']
    # 动作相关的配置，是否展示在顶部
    actions_on_top = True
    # 动作相关的配置，是否展示在底部
    actions_on_bottom = True
    # 保存、编辑、编辑并新建按钮是否在顶部展示 
    save_on_top = True

    # 展示自定义宇段
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id, ))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
