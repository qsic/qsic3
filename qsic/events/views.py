from django.conf import settings
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from qsic.core.utils import CalendarWeek
from qsic.events.models import Event
from qsic.events.models import Performance


def current_week(request):
    # get current week and forward to that week
    curr_week = CalendarWeek()
    return HttpResponseRedirect(reverse('qsic_week', args=(curr_week.slug,)))


# show calendar for week (Events & Performacnes without events)
def week(request, week_slug):
    cal_week = CalendarWeek(week_slug)

    # get all events starting this week
    events = [event for event in Event.objects.all() if event.start_dt in cal_week]
    # get all performances bound to an event
    event_performances = [p for p in event.performance_set.all() for event in events]

    # get all performances not in events
    performances = Performance.objects.filter(
        start_dt__gte=cal_week.start_dt,
        end_dt__lt=cal_week.end_dt,
        #not in=event_performances
    )

    return render_to_response(
        'events/week.html',
        locals(),
        context_instance=RequestContext(request)
    )


# show event (Particular Event with Performaces)
def event(request, event_id):
    # cheange to modelview
    event = Event.objects.get(event_id)

    return render_to_response(
        'events/event.html',
        locals(),
        context_instance=RequestContext(request)
    )


# show performance (Performance details)
def performance(request, performance_id):
    # change to modelveiw
    return render_to_response(
        'events/event.html',
        locals(),
        context_instance=RequestContext(request)
    )
