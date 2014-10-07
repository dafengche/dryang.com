from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'apps.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^demo/', include('demo.urls', namespace = 'demo')),
    url(r'^maccverif/', include('maccverif.urls', namespace = 'maccverif')),
    url(r'^admin/', include(admin.site.urls)),
)
