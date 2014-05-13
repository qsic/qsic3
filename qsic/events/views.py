import itertools
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import DetailView

from qsic.core.utils import CalendarWeek
from qsic.events.models import Event
from qsic.events.models import Performance

from django.template.defaultfilters import slugify


def tonight(request):

    return render_to_response(
        'events/tonight.html',
        locals(),
        context_instance=RequestContext(request)
    )


def current_week(request):
    # get current week and forward to that week
    cur_week = CalendarWeek()
    return HttpResponseRedirect(reverse('qsic_week', args=(cur_week.slug,)))


def week(request, week_slug):
    """
    Show calendar for week. Events along with their corresponding
    performances and performacnes without events.
    """
    cal_week = CalendarWeek(week_slug)

    # get all events for cal_week
    events = [e for e in Event.objects.all().order_by('_start_dt') if e.start_dt in cal_week]

    # get all performances not in events
    performances = Performance.objects.filter(
        start_dt__gte=cal_week.start_dt,
        start_dt__lt=cal_week.end_dt,
    ).exclude(
        event__in=events
    ).order_by(
        'start_dt'
    )

    events_and_perofrmances = list(itertools.chain(events, performances))

    events_and_perofrmances.sort(key=lambda i: i.start_dt)

    # for each day in ``cal_week``, add events and performances for that day
    # in the order they take place.
    days = []
    for day in cal_week.days():
        day_start = day['date']
        day_end = day['date'] + timedelta(days=1)

        day_events = []
        while (events_and_perofrmances and
                day_start <= events_and_perofrmances[0].start_dt < day_end):
            day_events.append(events_and_perofrmances.pop(0))
        days.append({'name': day['name'], 'date': day['date'], 'events': day_events})

    previous_week = cal_week - 1
    following_week = cal_week + 1

    return render_to_response(
        'events/week.html',
        locals(),
        context_instance=RequestContext(request)
    )


def current_month(request):
    # TODO
    pass


def month(request, month_slug):
    # TODO
    pass


def event_detial_view_add_slug(request, pk=None):
    e = get_object_or_404(Event, id=pk)
    return HttpResponseRedirect(e.url)


def performance_detail_view_add_slug(request, pk=None):
    p = get_object_or_404(Performance, id=pk)
    return HttpResponseRedirect(p.url)


class EventDetailView(DetailView):
    template_name = 'events/event_detail.html'
    model = Event


class PerformanceDetailView(DetailView):
    template_name = 'events/performance_detail.html'
    model = Performance