from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import DetailView
from django.views.generic import ListView

from qsic.groups.models import Group


def group_detail_view_add_slug(request, pk=None):
    g = get_object_or_404(Group, id=pk)
    return HttpResponseRedirect(g.url)


class GroupDetailView(DetailView):
    template_name = 'groups/group_detail.html'
    model = Group


class GroupListView(ListView):
    template_name = 'groups/group_list.html'
    model = Group

    filter_criteria = {}
    group_list_type = ''

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        queryset = self.model.objects.filter(**self.filter_criteria).order_by('-create_dt')

        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['group_list_type'] = self.group_list_type
        return context


class CurrentHouseTeamListView(GroupListView):
    group_list_type = 'Current House Teams'

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        queryset = super().get_queryset().filter(is_house_team=True)

        return [team for team in queryset if team.is_current]


class PastHouseTeamListView(GroupListView):
    group_list_type = 'Past House Teams'

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        queryset = super().get_queryset().filter(is_house_team=True)

        return [team for team in queryset if not team.is_current]


class VisitingGroupListView(GroupListView):
    group_list_type = 'Past and Present Visiting Teams'

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        queryset = super().get_queryset().filter(is_house_team=False)

        return [team for team in queryset if not team.is_current]