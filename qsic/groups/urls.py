from django.conf.urls import patterns
from django.conf.urls import url

from qsic.groups.views import GroupDetailView

urlpatterns = patterns(
    'qsic.groups.views',

    url(r'^house_teams/current/?$',
        'current_house_teams',
        name='qsic_current_house_teams'),

    url(r'^house_teams/past/?$',
        'past_house_teams',
        name='qsic_past_house_teams'),

    url(r'^group/(?P<slug>[A-Za-z0-9_\-]+)/?$',
        GroupDetailView.as_view(),
        name='group_detail_view'),
)
