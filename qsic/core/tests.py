from datetime import datetime
import unittest

from django.utils.timezone import utc

from freezegun import freeze_time

from .utils import CalendarWeek


class CalendarWeekTC(unittest.TestCase):

    def test_dt_from_slug_method(self):
        # Week of 2013-12-11 had a Monday on 2013-12-09
        expected = datetime(2013, 12, 9, 0, 0, 0, tzinfo=utc)
        result = CalendarWeek()._monday_dt_for_week_slug('20131211')
        self.assertEqual(expected, result)

    def test_dt_from_slug_instantiation(self):
        expected = datetime(2013, 12, 9, 0, 0, 0, tzinfo=utc)
        result = CalendarWeek('20131211').start_dt
        self.assertEqual(expected, result)

    @freeze_time("2013-12-11 01:23:45", tz_offset=-4)
    def test_start_dt_from_empty_instantiation(self):
        expected = datetime(2013, 12, 9, 0, 0, 0, tzinfo=utc)
        result = CalendarWeek().start_dt
        self.assertEqual(expected, result)

    def test_slug_from_cal_week(self):
        cal_week = CalendarWeek('20131211')
        self.assertEqual(cal_week.slug, '20131209')

    def test_end_dt_from_cal_week(self):
        expected = datetime(2013, 12, 16, 0, 0, 0, tzinfo=utc)
        result = CalendarWeek('20131211').end_dt
        self.assertEqual(expected, result)

    def test_days(self):
        expected = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
        cal_week = CalendarWeek('20131211')
        result = tuple(d['name'] for d in cal_week.days())
        self.assertEqual(expected, result)