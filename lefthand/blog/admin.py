from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Tag, Post
from .adminforms import PostAdminForm

from lefthand.base_admin import BaseOwnerAdmin
from lefthand.custom_site import custom_site


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count', 'owner')
    fields = ('name', 'status', 'is_nav', 'owner')

    # 显示分类下的文章数量
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = "文章数量"


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类 """
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status', 'owner')


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator',
    ]
    fieldsets = (
        ('基础配置', {
            'fields': (
                ('title', 'category'),
                'status', 'owner',
                'created_time',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('wide', ),
            'fields': ('tag', ),
        })
    )
    # 配置哪些字段可以作为链接
    list_display_links = []
    # 配置页面过滤器，需要通过哪些字段来过滤列表页
    list_filter = [CategoryOwnerFilter]
    # 配置搜索字段 
    search_fields = ['title', 'category__name']
    # 动作相关的配置，是否展示在顶部
    actions_on_top = True
    # 动作相关的配置，是否展示在底部
    actions_on_bottom = True
    # 保存、编辑、编辑并新建按钮是否在顶部展示 
    save_on_top = True
    # 横向展示字段
    filter_horizontal = ('tag', )
    # 纵向展示字段
    filter_vertical = ()

    # 展示自定义宇段
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id, ))
        )
    operator.short_description = '操作'


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id',
        'action_flag', 'user', 'change_message']
