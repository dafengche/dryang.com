from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.shortcuts import redirect

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'apps.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^welcome/', include('welcome.urls', namespace = 'dryang-welcome')),
    url(r'^demo/', include('demo.urls', namespace = 'dryang-demo')),
    url(r'^verif/', include('verif.urls', namespace = 'dryang-verif')),
    url(r'^badminton/', include('badminton.urls', namespace = 'dryang-badminton')),
    url(r'^auth/', include('common.auth.urls', namespace = 'dryang-auth')),
    url(r'^admin/', include(admin.site.urls)),
)
