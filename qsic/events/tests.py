from datetime import datetime

from django.test import TestCase
from django.utils.timezone import utc

from .models import Event
from .models import Performance


class EventDateTimeMethodsTC(TestCase):
    def setUp(self):
        self.e = Event.objects.create(name='TestEvent')

        self.p1 = Performance.objects.create(
            event=self.e,
            name='First Performace in Event',
            start_dt=datetime(2013, 1, 17, 19, 30, 0, tzinfo=utc),
            end_dt=datetime(2013, 1, 17, 20, 0, 0, tzinfo=utc)
        )

        self.p2 = Performance.objects.create(
            event=self.e,
            name='Second Performace in Event',
            start_dt=datetime(2013, 1, 17, 19, 45, 0, tzinfo=utc),
            end_dt=datetime(2013, 1, 17, 20, 15, 0, tzinfo=utc)
        )

        self.p3 = Performance.objects.create(
            event=None,
            name='Performace not in Event',
            start_dt=datetime(2013, 1, 17, 19, 30, 0, tzinfo=utc),
            end_dt=datetime(2013, 1, 17, 20, 0, 0, tzinfo=utc)
        )

    def test_event_start_dt_is_first_peformance_start_dt(self):
        self.assertEqual(Performance.objects.count(), 3)
        self.assertEqual(self.e.start_dt, self.p1.start_dt)

    def test_event_end_dt_is_last_peformance_end_dt(self):
        self.assertEqual(self.e.end_dt, self.p2.end_dt)

    def test_event_start_dt_overrides_performance_dt(self):
        dt = datetime(2013, 1, 17, 21, 45, 0, tzinfo=utc)
        self.e._start_dt = dt
        self.assertEqual(self.e.start_dt, dt)

    def test_event_end_dt_overrides_performance_dt(self):
        dt = datetime(2013, 1, 17, 22, 40, 0, tzinfo=utc)
        self.e._end_dt = dt
        self.assertEqual(self.e.end_dt, dt)


class EventPerformanceRelationTC(TestCase):
    def setUp(self):
        self.e = Event.objects.create(name='TestEvent')

        self.p1 = Performance.objects.create(
            event=self.e,
            name='First Performace in Event',
            start_dt=datetime(2013, 1, 17, 19, 30, 0, tzinfo=utc),
            end_dt=datetime(2013, 1, 17, 20, 0, 0, tzinfo=utc)
        )

        self.p2 = Performance.objects.create(
            event=self.e,
            name='Second Performace in Event',
            start_dt=datetime(2013, 1, 17, 19, 45, 0, tzinfo=utc),
            end_dt=datetime(2013, 1, 17, 20, 15, 0, tzinfo=utc)
        )

        self.p3 = Performance.objects.create(
            event=None,
            name='Performace not in Event',
            start_dt=datetime(2013, 1, 17, 19, 30, 0, tzinfo=utc),
            end_dt=datetime(2013, 1, 17, 20, 0, 0, tzinfo=utc)
        )

    def test_event_contains_correct_performances(self):
        self.assertIn(self.p1, self.e.performance_set.all())
        self.assertIn(self.p2, self.e.performance_set.all())
        self.assertNotIn(self.p3, self.e.performance_set.all())

    def test_iterability_of_event(self):
        expected = [self.p1, self.p2]
        result = [p for p in self.e]
        self.assertEqual(expected, result)


class EventsPerformacesWeekPassedToTemplateTC(TestCase):
    """
    Assert that correct event and week objects are handed to
    template for rendering.
    """

    def test_no_performaces_or_events_for_dark_week(self):
        response = self.client.get('/events/week/current', follow=True)
        local_context = [d for d in response.context if 'events' in d]
        self.assertIsNot(local_context, [])
        local_context = local_context[0]

        # make sure expect values are in local context

    def test_performances_no_events(self):
        pass

    def test_no_non_event_performances_several_events(self):
        pass

    def test_events_and_non_event_performances(self):
        pass
