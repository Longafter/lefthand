from django.urls import path

from .views import LinkListView

app_name = 'config'

urlpatterns = [
    path('links/', LinkListView.as_view(), name='links'),
]
