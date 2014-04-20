from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'homespun_site.views.home', name='home'),
    # url(r'^homespun_site/', include('homespun_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'homespun_terminal.views.home', name='home'),
    url(r'^chart/(?P<chart_type>\w+)/$', 'homespun_terminal.views.chart', name='chart'),
)

urlpatterns += staticfiles_urlpatterns()
