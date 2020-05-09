from django.contrib import admin

from .models import Link, SideBar

from lefthand.custom_site import custom_site


@admin.register(Link, site=custom_site)
class LinkAdmin(admin.ModelAdmin):
    list_dispaly = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)


@admin.register(SideBar, site=custom_site)
class SideBarAdmin(admin.ModelAdmin):
    list_dispaly = ('title', 'display_type', 'status', 'content', 'created_time')
    fields = ('title', 'display_type', 'status', 'content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
