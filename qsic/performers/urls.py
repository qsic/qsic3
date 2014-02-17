from django.conf.urls import patterns
from django.conf.urls import url

from qsic.performers.views import PerformerDetailView
from qsic.performers.views import PerformerListView


urlpatterns = patterns(
    'qsic.performers.views',

    url(r'^all$',
        PerformerListView.as_view(),
        name='qsic_performers'),

    url(r'^performer/(?P<pk>\d+)$',
        'performer_detail_view_add_slug',
        name='performer_detail_view_add_slug'),

    url(r'^performer/(?P<pk>\d+)/[A-Za-z0-9_\-]+$',
        PerformerDetailView.as_view(),
        name='performer_detail_view'),
)
