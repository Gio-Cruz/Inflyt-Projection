from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from projection import views
import projection

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home' , views.home_page),
    url(r'^astroProjection/$', views.astro_projection),
    url(r'^getTripPoints/(?P<startPoint>[^/]+)/(?P<endPoint>[^/]+)/(?P<distApart>[^/]+)/$', views.getTripPoints),
    
]