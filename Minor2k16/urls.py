import allauth
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from Cards import views
from Home import views as home_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', include('Cards.urls')),
    url(r'^api/(?P<key>[\w\-]+)/$', views.Cardlist.as_view()),
    url(r'^api_users', home_views.Usersinfolist.as_view()),
    url(r'^api_status', views.Statuslist.as_view()),
    url(r'^Home/', include('Home.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^boards/', include('Boards.urls')),
    url(r'^', include('alpha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


urlpatterns= format_suffix_patterns(urlpatterns)