from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'qsic.groups.views',

    url(r'^groups/?$',
        'current_week',
        name='qsic_current_week'),

    url(r'^group/(\d{8})/?$',
        'week',
        name='qsic_week'),
)
