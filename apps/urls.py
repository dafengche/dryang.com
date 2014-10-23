from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'apps.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^demo/', include('demo.urls', namespace = 'demo')),
    url(r'^verif/', include('verif.urls', namespace = 'verif')),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^admin/', include(admin.site.urls)),
)
