from django.conf.urls import patterns
from django.conf.urls import url

from events.views import EventDetailView
from events.views import PerformanceDetailView

urlpatterns = patterns(
    'events.views',

    url(r'^up-next/?$',
        'up_next',
        name='up_next'),

    url(r'^tonight/?$',
        'tonight',
        name='tonight'),

    url(r'^week/current/?$',
        'current_week',
        name='current_week'),

    url(r'^week/(\d{8})?$',
        'week',
        name='week'),

    # url(r'^month/current/?$',
    #     'current_month',
    #     name='qsic_current_month'),
    #
    # url(r'^month/(\d{6})?$',
    #     'month',
    #     name='qsic_month'),

    url(r'^event/(?P<pk>\d+)$',
        'event_detial_view_add_slug',
        name='event_detial_view_add_slug'),

    url(r'^performance/(?P<pk>\d+)$',
        'performance_detail_view_add_slug',
        name='performance_detail_view_add_slug'),

    url(r'^event/(?P<pk>\d+)/[A-Za-z0-9_\-]+$',
        EventDetailView.as_view(),
        name='event_detail_view'),

    url(r'^performance/(?P<pk>\d+)/[A-Za-z0-9_\-]+$',
        PerformanceDetailView.as_view(),
        name='peroformance_detail_view'),
)