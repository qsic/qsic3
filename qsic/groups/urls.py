from django.conf.urls import patterns
from django.conf.urls import url

from qsic.groups.views import GroupDetailView
from qsic.groups.views import CurrentHouseTeamListView
from qsic.groups.views import PastHouseTeamListView
from qsic.groups.views import VisitingGroupListView

urlpatterns = patterns(
    'qsic.groups.views',

    url(r'^house-teams/current$',
        CurrentHouseTeamListView.as_view(),
        name='qsic_current_house_teams'),

    url(r'^house-teams/past$',
        PastHouseTeamListView.as_view(),
        name='qsic_past_house_teams'),

    url(r'^visiting$',
        VisitingGroupListView.as_view(),
        name='qsic_visiting_groups'),

    url(r'^group/(?P<pk>\d+)$',
        'group_detail_view_add_slug',
        name='group_detail_view_add_slug'),

    url(r'^group/(?P<pk>\d+)/[A-Za-z0-9_\-]+$',
        GroupDetailView.as_view(),
        name='group_detail_view'),
)
