"""api URL Configuration"""
from django.conf.urls import url

from .views import CountListView

urlpatterns = [
    url(r'^$', CountListView.as_view(), name='counts')
]
