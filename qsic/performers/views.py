import datetime
from django.db.models import Q, Max
from django.views.generic import TemplateView,DetailView,ListView
from players.models import Player
from shows.models import TeamCalendar

class LoginView(TemplateView):
    model = Player
    template_name = 'login.html'

class PlayerDetailView(DetailView):
    model = Player

    def get_context_data(self, **kwargs):
        ctx = super(PlayerDetailView, self).get_context_data(**kwargs)
        teamset = ctx['player'].playerteam_set.prefetch_related('team').all()
        ctx['teams'] = {
            'active': [t.team for t in filter(lambda x: x.active == True, teamset)],
            'past': [t.team for t in filter(lambda x: x.active == False, teamset)],
        }
        ctx['placeholders'] = ['http://placebear.com/230/300', 'http://placebear.com/230/300', 'http://placekitten.com/230/300',
            'http://placepuppy.it/230/300', 'http://flickholdr.com/230/300/puppy', 'http://flickholdr.com/230/300/kitten',
            'http://flickholdr.com/230/300/turtle', 'http://flickholdr.com/230/300/dog', 'http://flickholdr.com/230/300/cat',
            'http://flickholdr.com/230/300/tortoise'
        ]
        ctx['upcoming_shows'] = TeamCalendar.objects.upcoming_team_shows(teamset)

        return ctx

class PlayersAllActiveView(ListView):
    context_object_name = 'player_list'
    template_name = 'players/all.html'

    def get_queryset(self):
        return Player.objects.filter(
            Q(playerteam__team__is_house_team=True) | Q(playerteam__team__teamcalendar__show__start_date__gte=datetime.datetime.now()),
            playerteam__active=True
        ).extra(
            select={'lower_last': 'lower(last_name)', 'lower_first': 'lower(first_name)'}
        ).order_by('lower_last', 'lower_first').distinct()

class PlayersAllPastView(PlayersAllActiveView):

    def get_context_data(self, **kwargs):
        ctx = super(PlayersAllPastView, self).get_context_data(**kwargs)
        ctx['past'] = True
        return ctx


    def get_queryset(self):
        return Player.objects.annotate(last_show=Max('playerteam__team__teamcalendar__show__start_date')).filter(
            Q(playerteam__active=False) | \
            Q(last_show__lt=datetime.datetime.now()) | \
            Q(last_show=None)
        ).extra(
            select={'lower_last': 'lower(last_name)', 'lower_first': 'lower(first_name)'}
        ).order_by('lower_last', 'lower_first').distinct()
