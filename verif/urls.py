from django.conf.urls import patterns, url

from verif import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    url(r'^get-plot/$', views.get_plot, name = 'get-plot'),
    url(r'^get-stations/$', views.get_stations, name = 'get-stations'),
    url(r'^test-group/$', views.test_group, name = 'test-group'),
)

