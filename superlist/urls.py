from django.conf.urls import url
from lists.views import home_page, view_list, new_list, add_item

from django.contrib import admin
from django.urls import path

urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^lists/new$', new_list, name='new_list'),
    url(r'^lists/(\d+)/$', view_list, name='view_list'),
    url(r'^lists/(\d+)/add_item$', add_item, name='add_item')
]
