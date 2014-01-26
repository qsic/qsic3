from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns(
    'qsic.events.views',

    url(r'^current_week/?$',
        'current_week',
        name='qsic_current_week'),

    url(r'^week/(\d{8})/?$',
        'week',
        name='qsic_week'),
)