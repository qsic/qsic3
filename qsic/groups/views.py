from django.conf import settings
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import DetailView

from qsic.groups.models import Group


class GroupDetailView(DetailView):
    template_name = 'group/group_detail.html'
    model = Group
    slug_field = 'slug'


def current_house_teams(request):

    teams = Group.objects.filter(is_house_team=True)
    teams = [t for t in teams if t.is_current]

    return render_to_response(
        'groups/house_team_list.html',
        locals(),
        context_instance=RequestContext(request)
    )


def past_house_teams(request):

    teams = Group.objects.filter(is_house_team=True)
    teams = [t for t in teams if not t.is_current]

    return render_to_response(
        'groups/house_team_list.html',
        locals(),
        context_instance=RequestContext(request)
    )
