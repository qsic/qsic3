from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'qsic.performers.views',

    url(r'^performers/?$',
        'current_week',
        name='qsic_performers'),

    url(r'^performers/(\d{8})/?$',
        'performer',
        name='qsic_performer_details'),
)
