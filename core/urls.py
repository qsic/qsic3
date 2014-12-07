from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',

    # to index page of QSIC
    url(r'^$', 'core.views.index_redirect', name='index'),

    # About Page
    url(r'^about/?$', TemplateView.as_view(template_name='core/about.html'), name='about'),
    url(r'^500/?$', TemplateView.as_view(template_name='500.html'), name='server_error'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()