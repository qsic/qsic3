from django.conf.urls import patterns, include, url
from players.views import LoginView, PlayerDetailView, PlayersAllActiveView, PlayersAllPastView

urlpatterns = patterns('',
    url('^login/$', LoginView.as_view()),
    url('^$', PlayersAllActiveView.as_view(), name='players_active'),
    url('^past/$', PlayersAllPastView.as_view(), name='players_past'),
    url('^(?P<pk>\d+)/(?P<name_slug>[-_\w]+)/$', PlayerDetailView.as_view(), name='player_detail'),

)

