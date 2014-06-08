from django.conf.urls import patterns
from django.conf.urls import url

from qsic.groups.views import GroupDetailView
from qsic.groups.views import CurrentHouseTeamListView
from qsic.groups.views import PastHouseTeamListView
from qsic.groups.views import VisitingGroupListView
from qsic.groups.views import AllPastGroupListView

urlpatterns = patterns(
    'qsic.groups.views',

    url(r'^house-teams/current$',
        CurrentHouseTeamListView.as_view(),
        name='current_house_teams'),

    url(r'^house-teams/past$',
        PastHouseTeamListView.as_view(),
        name='past_house_teams'),

    url(r'^visiting$',
        VisitingGroupListView.as_view(),
        name='visiting_groups'),

    url(r'all/past$',
        AllPastGroupListView.as_view(),
        name='past_groups'),

    url(r'^group/(?P<pk>\d+)$',
        'group_detail_view_add_slug',
        name='group_detail_view_add_slug'),

    url(r'^group/(?P<pk>\d+)/[A-Za-z0-9_\-]+$',
        GroupDetailView.as_view(),
        name='group_detail_view'),

    url(r'^load_from_it/(\d+)/?$',
        'load_from_it',
        name='load_group_from_it')
)
