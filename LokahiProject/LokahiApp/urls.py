from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^homepage/', views.homepage),
    url(r'^create_report/', views.create_report),
    url(r'^report/', views.report),
    #url(r'^result/', views.result),
    url(r'^result/(?P<pk>\d+)/$', views.result, name="result"),
    url(r'^$', views.index),
]

