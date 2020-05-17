import xadmin
from xadmin.filters import RelatedFieldListFilter
from xadmin.filters import manager
from xadmin.layout import Row, Fieldset, Container

from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Tag, Post
from .adminforms import PostAdminForm

from lefthand.base_admin import BaseOwnerAdmin


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count', 'owner')
    fields = ('name', 'status', 'is_nav', 'owner')

    # 显示分类下的文章数量
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = "文章数量"


class CategoryOwnerFilter(RelatedFieldListFilter):
    """ 自定义过滤器只展示当前用户分类 """

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status', 'owner')


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator'
    ]
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
    # 横向展示字段
    filter_horizontal = ('tag', )
    # 纵向展示字段
    filter_vertical = ()

    form_layout = (
        Fieldset(
            '基础信息',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'content',
        )
    )

    # 展示自定义宇段
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id, ))
        )
    operator.short_description = '操作'
