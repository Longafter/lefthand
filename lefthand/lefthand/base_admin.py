from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
        1. 自动补充分类，标签，文章，侧边栏，友链这些Model的Owner字段
        2. 针对 queryset 过滤当前用户数据
    """

    def save_model(self, request, obj, form, change):
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)