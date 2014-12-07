from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseServerError
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.conf import settings

from performers.models import Performer


def performer_detail_view_add_slug(request, pk=None):
    p = get_object_or_404(Performer, id=pk)
    return HttpResponseRedirect(p.url)


class PerformersRedirectView(RedirectView):
    def get_redirect_url(self):
        return reverse('performers:performers_current')


class PerformerDetailView(DetailView):
    template_name = 'performers/performer_detail.html'
    model = Performer

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['performer'] = self.object
        return context


class PerformerAllListView(ListView):
    template_name = 'performers/performer_list.html'
    model = Performer

    filter_criteria = {}
    performer_list_title = 'All Performers'

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        queryset = self.model.objects.filter(**self.filter_criteria).order_by('last_name')

        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['performer_list_type'] = self.performer_list_title
        return context


class PerformerCurrentListView(PerformerAllListView):
    filter_criteria = {'is_active': True}
    performer_list_title = 'Current Performers'


class PerformerPastListView(PerformerAllListView):
    filter_criteria = {'is_active': False}
    performer_list_title = 'Past Performers'


def load_from_it(request, qsic_id):
    performer = get_object_or_404(Performer, id=qsic_id)

    try:
        performer.load_from_it()
        messages.success(request, 'Success!')
    except:
        if settings.DEBUG:
            raise
        messages.error(request, 'There was an error loading info from Improvteams.com')

    return HttpResponseRedirect(reverse('admin:performer_change', args=(qsic_id,)))