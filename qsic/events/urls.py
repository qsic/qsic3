from django.conf.urls import patterns
from django.conf.urls import url

from qsic.events.views import EventDetailView
from qsic.events.views import PerformanceDetailView

urlpatterns = patterns(
    'qsic.events.views',

    url(r'^week/current/?$',
        'current_week',
        name='qsic_current_week'),

    url(r'^week/(\d{8})/?$',
        'week',
        name='qsic_week'),

    url(r'^event/(?P<pk>\d+)/?$',
        EventDetailView.as_view(),
        name='event_detail_view'),

    url(r'^performance/(?P<pk>\d+)/?$',
        PerformanceDetailView.as_view(),
        name='peroformance_detail_view'),
)