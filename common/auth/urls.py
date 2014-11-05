from django.conf.urls import patterns, url

from common.auth import views

urlpatterns = patterns('',
    url(r'^login/$', views.login, name = 'login'),
    url(r'^logout/$', views.logout, name = 'logout'),
    url(r'^access-denied/$', views.access_denied, name = 'access-denied'),
)

