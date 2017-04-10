from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^register/', CreateView.as_view(
            template_name='register.html',
            form_class=UserCreationForm,
            success_url='/'
    )),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^login/', auth_views.login, name='login'),
    # Logging out takes you back to the landing page
    url(r'^logout/$', auth_views.logout, {'template_name': 'index.html'}, name='logout'),
    url(r'^homepage/', views.homepage, name="homepage"),
    url(r'^report/new/$', views.create_report, name="create_report"),
    url(r'^report/', views.report),
    url(r'^result/(?P<pk>\d+)/$', views.result, name="result"),
    url(r'^result/(?P<pk>\d+)/edit/$', views.report_edit, name='report_edit'),
    url(r'^submit', views.submit),
    url(r'^$', views.index),
]

