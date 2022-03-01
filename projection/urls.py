from django.contrib import admin
from django.urls import path
from django.urls import re_path
from projection import views
import projection

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home' , views.home_page),
    re_path(r'^astroProjection/$', views.astro_projection),
    re_path(r'^getTripPoints/(?P<startPoint>[^/]+)/(?P<endPoint>[^/]+)/(?P<distApart>[^/]+)/$', views.getTripPoints),
    re_path(r'^getCelestial/(?P<lat>[^/]+)/(?P<long>[^/]+)/$', views.getCelestial),
    re_path(r'^getIDNames/(?P<ra>[^/]+)/(?P<dec>[^/]+)/$', views.getIDNames)
    
]