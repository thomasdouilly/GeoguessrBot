from django.contrib import admin
from django.urls import path, re_path
from send_gps_values import views


urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^screen_capture/$', views.screen_capture, name='screen_capture'),
    re_path(r'^reset_pictures/$', views.reset_pictures, name='reset_pictures'),
    re_path(r'^process/$', views.process, name='process'),
    re_path(r'^reload/$', views.reload, name='reload'),
]