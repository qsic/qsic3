from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView

from qsic.performers.models import Performer


def performer_detail_view_add_slug(request, pk=None):
    p = get_object_or_404(Performer, id=pk)
    return HttpResponseRedirect(p.url)


class PerformerDetailView(DetailView):
    template_name = 'performers/performer_detail.html'
    model = Performer


class PerformerListView(ListView):
    template_name = 'performers/performer_list.html'
    model = Performer



