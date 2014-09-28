from django.conf.urls import patterns, url

from demo import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    url(r'^calc/$', views.calc, name = 'calc'),
)

