from django.conf.urls import url
from django.contrib import admin

#importing views
#we need to create views.py
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #define the url getdata that we have written inside form
    url(r'^login/', views.login),
    url(r'^homepage/', views.homepage),
    url(r'^create_report/', views.create_report),
    url(r'^report/', views.report),

   #defining the view for root URL
    url(r'^$', views.index),
]