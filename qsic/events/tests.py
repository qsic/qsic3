import unittest
from datetime import datetime

from django.template.defaultfilters import slugify
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone

from freezegun import freeze_time

from qsic.core.utils import EST

from .models import Event
from .models import Performance
from .models import ReoccurringEventType

from qsic.core.utils import CalendarWeek


class EventDateTimeMethodsTC(TestCase):
    def setUp(self):
        self.e = Event.objects.create(name='TestEvent')

        self.p1 = Performance.objects.create(
            event=self.e,
            name='First Performace in Event',
            start_dt=datetime(2013, 1, 17, 19, 30, 0, tzinfo=EST),
            end_dt=datetime(2013, 1, 17, 20, 0, 0, tzinfo=EST)
        )

        self.p2 = Performance.objects.create(
            event=self.e,
            name='Second Performace in Event',
            start_dt=datetime(2013, 1, 17, 19, 45, 0, tzinfo=EST),
            end_dt=datetime(2013, 1, 17, 20, 15, 0, tzinfo=EST)
        )

        self.p3 = Performance.objects.create(
            event=None,
            name='Performace not in Event',
            start_dt=datetime(2013, 1, 17, 19, 30, 0, tzinfo=EST),
            end_dt=datetime(2013, 1, 17, 20, 0, 0, tzinfo=EST)
        )

    def test_event_start_dt_is_first_peformance_start_dt(self):
        self.assertEqual(Performance.objects.count(), 3)
        self.assertEqual(self.e.start_dt, self.p1.start_dt)

    def test_event_end_dt_is_last_peformance_end_dt(self):
        self.assertEqual(self.e.end_dt, self.p2.end_dt)

    def test_event_start_dt_overrides_performance_dt(self):
        dt = datetime(2013, 1, 17, 21, 45, 0, tzinfo=EST)
        self.e._start_dt = dt
        self.assertEqual(self.e.start_dt, dt)

    def test_event_end_dt_overrides_performance_dt(self):
        dt = datetime(2013, 1, 17, 22, 40, 0, tzinfo=EST)
        self.e._end_dt = dt
        self.assertEqual(self.e.end_dt, dt)


class EventPerformanceRelationTC(TestCase):
    def setUp(self):
        self.e = Event.objects.create(name='TestEvent')

        self.p1 = Performance.objects.create(
            event=self.e,
            name='First Performace in Event',
            start_dt=datetime(2013, 1, 17, 19, 30, 0, tzinfo=EST),
            end_dt=datetime(2013, 1, 17, 20, 0, 0, tzinfo=EST)
        )

        self.p2 = Performance.objects.create(
            event=self.e,
            name='Second Performace in Event',
            start_dt=datetime(2013, 1, 17, 19, 45, 0, tzinfo=EST),
            end_dt=datetime(2013, 1, 17, 20, 15, 0, tzinfo=EST)
        )

        self.p3 = Performance.objects.create(
            event=None,
            name='Performace not in Event',
            start_dt=datetime(2013, 1, 17, 19, 30, 0, tzinfo=EST),
            end_dt=datetime(2013, 1, 17, 20, 0, 0, tzinfo=EST)
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
    Assert that correct event and performances objects are handed to
    template for rendering.
    """
    def setUp(self):
        """
        Set up events and performances for next several weeks
        """
        self.cal_week = CalendarWeek()

        # Week of Monday, 2012-12-10 - One Event, Winter Ball
        self.e1 = Event.objects.create(
            name='QSIC Winter Ball',
            description='A night of fun!',
            _start_dt=datetime(2012, 12, 15, 21, 0, 0, tzinfo=EST),
            _end_dt=datetime(2012, 12, 16, 2, 0, 0, tzinfo=EST),
            _price=15.00
        )

        # Week of Monday, 2012-12-17 - One event with two performances
        self.e2 = Event.objects.create(name='QSIC House Night', description='A night of fun!')
        self.p1 = Performance.objects.create(
            event=self.e2,
            name='Peace Love and Joy',
            start_dt=datetime(2012, 12, 21, 19, 30, 0, tzinfo=EST),
            end_dt=datetime(2012, 12, 21, 20, 0, 0, tzinfo=EST),
            price=5.00
        )
        self.p2 = Performance.objects.create(
            event=self.e2,
            name="Rockin' Rolla Music",
            start_dt=datetime(2012, 12, 21, 20, 0, 0, tzinfo=EST),
            end_dt=datetime(2012, 12, 21, 20, 30, 0, tzinfo=EST),
            price=5.00
        )

        # Week of Monday, 2012-12-24 - Dark

        # Week of Monday, 2012-12-31 - No events, 3 performances
        self.p3 = Performance.objects.create(
            event=self.e2,
            name='Suzie Q & The Team',
            start_dt=datetime(2013, 1, 2, 20, 15, 0, tzinfo=EST),
            end_dt=datetime(2013, 1, 2, 23, 0, 0, tzinfo=EST),
            price=5.00
        )
        self.p4 = Performance.objects.create(
            event=self.e2,
            name='Magic Man, The',
            start_dt=datetime(2013, 1, 4, 19, 0, 0, tzinfo=EST),
            end_dt=datetime(2012, 1, 4, 21, 15, 0, tzinfo=EST),
            price=5.00
        )
        self.p5 = Performance.objects.create(
            event=self.e2,
            name='Marty Loves Pizza',
            start_dt=datetime(2013, 1, 5, 12, 30, 0, tzinfo=EST),
            end_dt=datetime(2012, 1, 5, 16, 0, 0, tzinfo=EST),
            price=5.00
        )

        # Week of Monday, 2013-01-07 - 1 events, 2 performances in event, 1 not in event
        self.e3 = Event.objects.create(name='Happy Fun Time', description='Lalalalalal')
        self.p6 = Performance.objects.create(
            event=self.e3,
            name='Skiddss',
            start_dt=datetime(2013, 1, 11, 15, 0, 0, tzinfo=EST),
            end_dt=datetime(2012, 1, 11, 17, 0, 0, tzinfo=EST),
            price=23.00
        )
        self.p7 = Performance.objects.create(
            event=self.e3,
            name='Lolipops',
            start_dt=datetime(2013, 1, 11, 17, 30, 0, tzinfo=EST),
            end_dt=datetime(2012, 1, 11, 19, 0, 0, tzinfo=EST),
            price=34.00
        )
        self.p8 = Performance.objects.create(
            name='Madness!',
            start_dt=datetime(2013, 1, 11, 20, 30, 0, tzinfo=EST),
            end_dt=datetime(2012, 1, 11, 22, 0, 0, tzinfo=EST),
            price=15.00
        )

    def get_local_context(self, response):
        self.assertTrue(hasattr(response, 'context'))
        context = response.context
        return {'events': context['events'], 'performances': context['performances']}

    def test_no_performaces_or_events_for_dark_week(self):
        response = self.client.get('/events/week/20121224', follow=True)
        local_context = self.get_local_context(response)
        # Assert no events
        self.assertEqual(local_context['events'], [])
        # Assert no Performances
        self.assertEqual([p for p in local_context['performances']], [])

    def test_performances_no_events(self):
        response = self.client.get('/events/week/20121231', follow=True)
        local_context = self.get_local_context(response)
        # Assert no events
        self.assertEqual(local_context['events'], [])
        # 3 Performances
        self.assertEqual(local_context['performances'].count(), 3)

    def test_no_non_event_performances_one_event(self):
        response = self.client.get('/events/week/20121217', follow=True)
        local_context = self.get_local_context(response)
        # Assert 1 event
        self.assertEqual(len([e for e in local_context['events']]), 1)
        # No Performances
        self.assertEqual(local_context['performances'].count(), 0)

    def test_events_and_non_event_performances(self):
        response = self.client.get('/events/week/20130107', follow=True)
        local_context = self.get_local_context(response)
        # Assert 1 event
        events = [e for e in local_context['events']]
        self.assertEqual(len(events), 1)
        event_performances = [p for p in events[0]]
        # 2 Event Performances
        self.assertEqual(len(event_performances), 2)
        # 1 Non Event Performance
        self.assertEqual(local_context['performances'].count(), 1)


# "2012-12-12 00:00:00" is a Wednesday
# 15th is a Saturday
@freeze_time("2012-12-12 00:00:00", tz_offset=-4)
class EventsPerformacesDetailViewContextPassedToTemplateTC(TestCase):
    """
    Assert that correct event and performance objects are handed to
    template for rendering.
    """
    def setUp(self):
        """
        Set up an event and some performances.
        """
        self.cal_week = CalendarWeek()

        # Week of Monday, 2012-12-17 - One event with two performances
        self.e1 = Event.objects.create(name='QSIC House Night', description='A night of fun!')
        self.p1 = Performance.objects.create(
            event=self.e1,
            name='Peace Love and Joy',
            start_dt=datetime(2012, 12, 21, 19, 30, 0, tzinfo=EST),
            end_dt=datetime(2012, 12, 21, 20, 0, 0, tzinfo=EST),
            price=5.00
        )
        self.p2 = Performance.objects.create(
            event=self.e1,
            name="Rockin' Rolla Music",
            start_dt=datetime(2012, 12, 21, 20, 0, 0, tzinfo=EST),
            end_dt=datetime(2012, 12, 21, 20, 30, 0, tzinfo=EST),
            price=5.00
        )

    def test_event_in_context(self):
        response = self.client.get('/events/event/' + str(self.e1.id), follow=True)
        self.assertTrue(hasattr(response, 'context_data'))
        local_context = response.context_data
        self.assertEqual(local_context['event'], self.e1)

    def test_performance_in_context_no_event(self):
        response = self.client.get('/events/performance/' + str(self.p1.id), follow=True)
        self.assertTrue(hasattr(response, 'context_data'))
        local_context = response.context_data
        self.assertEqual(local_context['performance'], self.p1)
        self.assertFalse(hasattr(local_context, 'event'))


class SlugTC(TestCase):
    """
    A test case for all slug related tests.
    """
    @classmethod
    def setUpClass(cls):
        cls.start_dt = datetime.now().replace(tzinfo=EST)
        cls.end_dt = datetime.now().replace(tzinfo=EST)

    def test_save_event_generates_correct_slug(self):
        e = Event.objects.create(name='QSIC House Night')
        self.assertEqual(e.slug, 'qsic-house-night')

    def test_save_performance_generates_correct_slug(self):
        p = Performance.objects.create(name='Butter High!',
                                       start_dt=self.start_dt,
                                       end_dt=self.end_dt)
        self.assertEqual(p.slug, 'butter-high')

    def test_get_event_detail_view_redirects_to_view_with_slug(self):
        e = Event.objects.create(name='QSIC House Night')
        response = self.client.get('/events/event/' + str(e.id), follow=True)
        self.assertTrue(hasattr(response, 'request'))
        self.assertEqual(response.request['PATH_INFO'], e.url)

    def test_get_performance_detail_view_redirects_to_view_with_slug(self):
        p = Performance.objects.create(name='Butter High!',
                                       start_dt=self.start_dt,
                                       end_dt=self.end_dt)
        response = self.client.get('/events/performance/' + str(p.id), follow=True)
        self.assertTrue(hasattr(response, 'request'))
        self.assertEqual(response.request['PATH_INFO'], p.url)


class ReoccuringEventsTC(TestCase):
    def test_build_reoccuring_events(self):
        event_start_time = datetime(2014, 6, 20, 19, 30, 0, tzinfo=EST)
        event_end_time = datetime(2014, 6, 20, 22, 30, 0, tzinfo=EST)
        ret = ReoccurringEventType.objects.create(name='Test events', period=7)
        e = Event.objects.create(name='TestEvent',
                                 description='Lots of fun here',
                                 reoccurring_event_type=ret,
                                 _start_dt=event_start_time,
                                 _end_dt=event_end_time)
        self.assertEqual(Event.objects.count(), 1)
        # go to up-next page 8 days prior to event's start date
        with freeze_time('2014-06-12 00:00:00', tz_offset=-4):
            self.client.get(reverse('qsic:up_next'), follow=True)
        self.assertEqual(Event.objects.count(), 1)
        # go to page 4 days prior to event's start date
        with freeze_time('2014-06-16 00:00:00', tz_offset=-4):
            self.client.get(reverse('qsic:up_next'), follow=True)
        e_qs = Event.objects.order_by('-_start_dt')
        self.assertEqual(e_qs.count(), 2)
        self.assertEqual(e_qs.first().start_dt, e.start_dt + timezone.timedelta(days=7))
        # go to page 2 days after event's start date
        with freeze_time('2014-06-22 00:00:00', tz_offset=-4):
            self.client.get(reverse('qsic:up_next'), follow=True)
        self.assertEqual(Event.objects.count(), 3)
        e_qs = Event.objects.order_by('-_start_dt')
        self.assertEqual(e_qs.first().start_dt, e.start_dt + timezone.timedelta(days=14))