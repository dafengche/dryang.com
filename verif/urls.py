from django.conf.urls import patterns, url

from verif import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    url(r'^get-plot/$', views.get_plot, name = 'get-plot'),
)

