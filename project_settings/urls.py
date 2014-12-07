from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qsic3.views.home', name='home'),
    # url(r'^qsic3/', include('qsic3.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # sub apps
    url(r'', include('core.urls', namespace='core')),
    url(r'^events/', include('events.urls', namespace='events')),
    url(r'^groups/', include('groups.urls', namespace='groups')),
    url(r'^performers/', include('performers.urls', namespace='performers')),
)
