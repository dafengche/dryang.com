from django.conf.urls import patterns, url

from badminton import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    url(r'^list/$', views.list, name = 'list'),
)

