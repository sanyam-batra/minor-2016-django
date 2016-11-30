from django.conf.urls import url
from Boards import views
from Cards import views as card_views

app_name = "boards"

urlpatterns = [

    url(r'^$', views.boards_add, name='boards_add'),
    url(r'^b/(?P<idd>[\w\-]+)/$', views.list_add, name='list-add'),
    url(r'delete/(?P<pk>[\w\-]+)/$',views.DeleteBoard.as_view(), name='delete_board'),
    url(r'delete/list/(?P<pk>[\w\-]+)/$',views.DeleteList.as_view(), name='delete_list')

]
