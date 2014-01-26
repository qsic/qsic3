from django.conf import settings
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from qsic.core.utils import CalendarWeek


def current_week(request):
    # get current week and forward to that week
    curr_week = CalendarWeek()
    return HttpResponseRedirect(reverse('qsic_week', args=(curr_week.slug,)))


# show calendar for date (Events & Performacnes without events)
def week(request, week_slug):


    return render_to_response(
        'events/week.html',
        locals(),
        context_instance=RequestContext(request)
    )


# show event (Particular Event with Performaces)



# show performance (Performance details)
# show calendar for week (Events & Performances without events)
