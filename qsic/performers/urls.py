from django.conf.urls import patterns
from django.conf.urls import url

from qsic.performers.views import PerformersRedirectView
from qsic.performers.views import PerformerDetailView
from qsic.performers.views import PerformerAllListView
from qsic.performers.views import PerformerPastListView
from qsic.performers.views import PerformerCurrentListView


urlpatterns = patterns(
    'qsic.performers.views',

    url(r'^$',
        PerformersRedirectView.as_view(),
        name='qsic_performers_index'),

    url(r'^all/?$',
        PerformerAllListView.as_view(),
        name='qsic_performers_all'),

    url(r'^current/?$',
        PerformerCurrentListView.as_view(),
        name='qsic_performers_current'),

    url(r'^past/?$',
        PerformerPastListView.as_view(),
        name='qsic_performers_past'),

    url(r'^performer/(?P<pk>\d+)/?$',
        'performer_detail_view_add_slug',
        name='performer_detail_view_add_slug'),

    url(r'^performer/(?P<pk>\d+)/[A-Za-z0-9_\-]+/?$',
        PerformerDetailView.as_view(),
        name='performer_detail_view'),
)
