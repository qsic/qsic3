from django.conf.urls import patterns
from django.conf.urls import url

from performers.views import PerformersRedirectView
from performers.views import PerformerDetailView
from performers.views import PerformerAllListView
from performers.views import PerformerPastListView
from performers.views import PerformerCurrentListView


urlpatterns = patterns(
    'performers.views',

    url(r'^$',
        PerformersRedirectView.as_view(),
        name='performers_index'),

    url(r'^all/?$',
        PerformerAllListView.as_view(),
        name='performers_all'),

    url(r'^current/?$',
        PerformerCurrentListView.as_view(),
        name='performers_current'),

    url(r'^past/?$',
        PerformerPastListView.as_view(),
        name='performers_past'),

    url(r'^performer/(?P<pk>\d+)/?$',
        'performer_detail_view_add_slug',
        name='performer_detail_view_add_slug'),

    url(r'^performer/(?P<pk>\d+)/[A-Za-z0-9_\-]+/?$',
        PerformerDetailView.as_view(),
        name='performer_detail_view'),

    url(r'^load_from_it/(\d+)/?$',
        'load_from_it',
        name='load_performer_from_it')
)
