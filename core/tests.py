import unittest

from django.utils import timezone

from freezegun import freeze_time

from .utils import CalendarWeek
from .utils import EST


class CalendarWeekTC(unittest.TestCase):

    def test_dt_from_slug_method(self):
        # Week of 2013-12-11 had a Monday on 2013-12-09
        expected = timezone.datetime(2013, 12, 9, 0, 0, 0, 0, tzinfo=EST)
        result = CalendarWeek()._monday_dt_for_week_slug('20131211')
        self.assertEqual(expected, result)

    def test_dt_from_slug_instantiation(self):
        expected = timezone.datetime(2013, 12, 9, 0, 0, 0, 0, tzinfo=EST)
        result = CalendarWeek('20131211').start_dt
        self.assertEqual(expected, result)

    @freeze_time("2013-12-11 01:23:45.39")
    def test_start_dt_from_empty_instantiation(self):
        expected = timezone.datetime(2013, 12, 9, 0, 0, 0, 0, tzinfo=EST)
        result = CalendarWeek().start_dt
        self.assertEqual(expected, result)

    def test_slug_from_cal_week(self):
        cal_week = CalendarWeek('20131211')
        self.assertEqual(cal_week.slug, '20131209')

    def test_end_dt_from_cal_week(self):
        expected = timezone.datetime(2013, 12, 16, 0, 0, 0, 0, tzinfo=EST)
        result = CalendarWeek('20131211').end_dt
        self.assertEqual(expected, result)

    def test_days(self):
        expected = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
        cal_week = CalendarWeek('20131211')
        result = tuple(d['name'] for d in cal_week.days())
        self.assertEqual(expected, result)

    def test_add_int_to_calendar_week(self):
        cal_week = CalendarWeek('20140217')
        next_cal_week = cal_week + 1
        self.assertIsInstance(next_cal_week, CalendarWeek)
        self.assertEqual(next_cal_week.slug, '20140224')

    def test_sub_int_from_calendar_week(self):
        cal_week = CalendarWeek('20140217')
        prev_cal_week = cal_week - 1
        self.assertIsInstance(prev_cal_week, CalendarWeek)
        self.assertEqual(prev_cal_week.slug, '20140210')

    def test_calendar_week_start_dt_must_be_datetime(self):
        with self.assertRaises(ValueError):
            CalendarWeek(start_dt='moo')

    def test_calendar_week_start_dt_time_must_be_zeroed(self):
        cal_week = CalendarWeek('20140217')
        with freeze_time("2014-02-17 01:00:00.0"), self.assertRaises(ValueError):
            cal_week.start_dt = timezone.now()
        with freeze_time("2014-02-17 00:01:00.0"), self.assertRaises(ValueError):
            cal_week.start_dt = timezone.now()
        with freeze_time("2014-02-17 00:00:01.0"), self.assertRaises(ValueError):
            cal_week.start_dt = timezone.now()
        with freeze_time("2014-02-17 00:00:00.1"), self.assertRaises(ValueError):
            cal_week.start_dt = timezone.now()

    def test_calendar_week_start_dt_must_have_tzinfo_set_to_est(self):
        cal_week = CalendarWeek('20140217')
        with self.assertRaises(ValueError):
            cal_week.start_dt = timezone.datetime(2014, 2, 17, tzinfo=timezone.utc)

        cal_week.start_dt = timezone.datetime(2014, 2, 17, tzinfo=EST)

        cal_week.start_dt = timezone.datetime(2014, 2, 17,
                                              tzinfo=timezone.pytz.timezone('US/Eastern'))

    def test_calendar_week_init_with_a_monday_sets_itself_to_that_monday(self):
        cal_week = CalendarWeek('20140217')
        self.assertEqual(cal_week.start_dt, timezone.datetime(2014, 2, 17, tzinfo=EST))

    def test_is_current_week(self):
        cal_week = CalendarWeek('20140217')

        with freeze_time("2014-02-18 01:23:45"):
            self.assertTrue(cal_week.is_current_week())

        with freeze_time("2014-01-18 01:23:45"):
            self.assertFalse(cal_week.is_current_week())
