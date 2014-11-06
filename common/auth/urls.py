from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

from common.auth import views

urlpatterns = patterns('',
    url(r'^login/$', views.login, name = 'login'),
    url(r'^logout/$', views.logout, name = 'logout'),
#    url(r'^access-denied/$', views.access_denied, name = 'access-denied'),
    url(r'^access-denied/$', TemplateView.as_view(template_name = 'auth/access-denied.html'), name = 'access-denied'),
)

