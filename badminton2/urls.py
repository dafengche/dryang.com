from django.conf.urls import patterns, url

from badminton2 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    url(r'^get-data/$', views.get_data, name = 'get-data'),
)

