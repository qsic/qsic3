from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',

    # to index page of QSIC
    url(r'^$', 'qsic.views.index_redirect', name='qsic_index'),

    # About Page
    url(r'^about/?$', TemplateView.as_view(template_name='about.html')),

    # sub apps
    url(r'^events/', include('qsic.events.urls')),
    url(r'^groups/', include('qsic.groups.urls')),
    url(r'^performers/', include('qsic.performers.urls')),

)

urlpatterns += staticfiles_urlpatterns()