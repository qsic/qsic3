from django.utils import timezone

from .models import Event
from .models import ReoccurringEventType


LAST_CALCULATED = timezone.now()


def build_reoccuring_events(start_ts, memoize=False):
    if memoize and timezone.now() - LAST_CALCULATED < timezone.timedelta(hours=1):
        return

    # Given a week start time, are there any reoccuring event types that
    # do not have an associated event. If so, create an event for each
    # ``ReoccurringEventType``.
    ret_qs = ReoccurringEventType.objects.all()
    for ret in ret_qs:
        last_event_of_type = ret.event_set.order_by('-_start_dt').first()
        if not last_event_of_type:
            continue

        if last_event_of_type.start_dt - start_ts < timezone.timedelta(days=ret.period):
            # make new event by copying the last event
            e = Event.objects.create(
                name=last_event_of_type.name,
                slug=last_event_of_type.slug,
                _start_dt=last_event_of_type.start_dt + timezone.timedelta(days=ret.period),
                _end_dt=last_event_of_type.end_dt + timezone.timedelta(days=ret.period),
                _price=last_event_of_type._price,
                description=last_event_of_type.description,
                reoccurring_event_type=ret,
            )

    LAST_CALCULATED = timezone.now()