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


#
def week(request, week_slug):
    """
    Show calendar for week. Events along with their corresponding
    performances and performacnes without events.
    """
    cal_week = CalendarWeek(week_slug)

    # get all events for cal_week
    events = (e for e in Event.objects.all() if e.start_dt in cal_week)

    # get all performances not in events
    performances = Performance.objects.filter(
        start_dt__gte=cal_week.start_dt,
        end_dt__lt=cal_week.end_dt,
    ).exclude(
        event__in=events
    )

    party_var = 'WOOOO!!!'
    party_dict = {'first': 'FIEIFEIFJEI'}
    party_list = ['maybe']

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
