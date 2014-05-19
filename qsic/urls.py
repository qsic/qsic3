from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',

    # to index page of QSIC
    url(r'^$', 'qsic.views.index_redirect', name='index'),

    # About Page
    url(r'^about/?$', TemplateView.as_view(template_name='about.html'), name='about'),

    # sub apps
    url(r'^events/', include('qsic.events.urls')),
    url(r'^groups/', include('qsic.groups.urls')),
    url(r'^performers/', include('qsic.performers.urls')),

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()