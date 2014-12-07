"""
This module defines some core utilities used throughout
the QSIC website.
"""
from datetime import datetime
from datetime import timedelta

from django.utils.timezone import utc
import pytz

EST = pytz.timezone('US/Eastern')


def validate_slug(slug, digits=8):
    """
    Return true if a slug is a string and has the correct number of digits.
    """
    return isinstance(slug, str) and len(slug) == digits


class CalendarWeek(object):
    """
    This class represents a Sun - Sat week.
    Weeks start on Monday at 00:00:00 EST and ends instantaniously before
    00:00:00 EST on the following Monday.
    """
    slug_pattern = '%Y%m%d'

    def __init__(self, slug=None, start_dt=None):
        """
        Initialize a CalendarWeek object.

        Initialize with a slug of the form ``\d{8}`` or
        a datetime instance set to a Monday at 00:00:00 EST.
        If no kwargs are given, create a ``CalendarWeek``
        with a ``start_dt` set to the most recently past
        Monday, 00:00:00 EST.
        """
        # referecnes Monday, 00:00:00 EST of the given week
        if start_dt:
            self.start_dt = start_dt
        elif slug:
            self.start_dt = self._monday_dt_for_week_slug(slug)
        else:
            self.start_dt = self._get_most_recent_past_monday_est(datetime.now())

    @staticmethod
    def _get_most_recent_past_monday_est(dt):
        """
        Return a datetime instance with its date set to the most recent
        Monday relative to the instance's original datetime
        and a time set to 00:00:00 EST.
        """
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=EST)
        # calculate offset from today to most recent past Monday
        # Monday (0), Sunday (7)
        dt = dt - timedelta(days=dt.weekday())
        return dt

    def _monday_dt_for_week_slug(self, slug):
        """
        Return most recent past sunday's tz-aware datetime based on YYYYMMDD slug.
        """
        # get datetime based on slug
        if slug and validate_slug(slug):
            dt = datetime.strptime(slug, self.slug_pattern)
        else:
            raise ValueError('Invalid slug given. {}'.format(slug))

        return self._get_most_recent_past_monday_est(dt)

    @property
    def start_dt(self):
        return self._start_dt

    @start_dt.setter
    def start_dt(self, dt):
        if not isinstance(dt, datetime):
            raise ValueError('CalendarWeek.start_dt must be of type {}. '
                             'Got object of type {} instead'.format(datetime, type(dt)))

        if not (dt.hour, dt.minute, dt.second, dt.microsecond) == (0, 0, 0, 0):
            raise ValueError('CalendarWeek.start_dt can only be set to '
                             'a Monday with a time of 00:00:00.000000. '
                             'Time given: {}'.format(dt.time()))

        if not dt.tzinfo == EST:
            raise ValueError('CalendarWeek.start_dt can only have a tzinfo value of `EST`')

        self._start_dt = dt

    @property
    def end_dt(self):
        return self.start_dt + timedelta(weeks=1)

    def __add__(self, other):
        if not isinstance(other, int):
            raise ValueError('Expected integer value. Got {}'.format(type(other)))
        return CalendarWeek(start_dt=self.start_dt + timedelta(weeks=other))

    def __sub__(self, other):
        if not isinstance(other, int):
            raise ValueError('Expected integer value. Got {}'.format(type(other)))
        return CalendarWeek(start_dt=self.start_dt - timedelta(weeks=other))

    @property
    def slug(self):
        """
        Return string which can be used in urls identifying week by YYYYMMDD.
        """
        return self.start_dt.strftime(self.slug_pattern)

    def __str__(self):
        return self.start_dt.strftime('%Y-%m-%d')

    def __contains__(self, item):
        if isinstance(item, str) and len(item) == 8:
            return self.start_dt == self._monday_dt_for_week_slug(item)
        elif isinstance(item, datetime):
            return self.start_dt <= item < self.end_dt
        return False

    def days(self):
        days = []
        for i in range(7):
            date = self.start_dt + timedelta(days=i)
            days.append({
                'date': date,
                'name': date.strftime('%A'),
                'offset': i
            })
        return days

    def is_current_week(self):
        return self.start_dt == CalendarWeek().start_dt