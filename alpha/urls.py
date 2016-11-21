from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^loginchat/$', views.Login, name='login'),
    url(r'^logoutchat/$', views.Logout, name='logout'),
    url(r'^homechat/$', views.Home, name='home'),
    url(r'^post/$', views.Post, name='post'),
    url(r'^messages/$', views.Messages, name='messages'),
]