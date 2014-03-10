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

    def __init__(self, slug=None):
        """
        Initialize a CalendarWeek object with a slug of the form \d{8}
        If a naive datetime or no datetimme is given, create one based on
        current date.
        """
        # referecnes Monday, 00:00:00 EST of the given week
        self._start_dt = self._monday_dt_for_week_slug(slug)

    def _monday_dt_for_week_slug(self, slug=None):
        """
        Return most recent past sunday's tz-aware datetime based on YYYYMMDD slug.
        """
        # get datetime based on slug
        if slug and validate_slug(slug):
            dt = datetime.strptime(slug, self.slug_pattern)
        else:
            dt = datetime.now().replace(hour=0, minute=0, second=0)
        dt = dt.replace(tzinfo=EST)

        # calculate offset from today to most recent past Monday
        # Monday (0), Sunday (7)
        dt = dt - timedelta(days=dt.weekday())
        return dt

    @property
    def start_dt(self):
        return self._start_dt

    @property
    def end_dt(self):
        return self.start_dt + timedelta(weeks=1)

    def __add__(self, other):
        if not isinstance(other, int):
            raise ValueError('Expected integer value. Got {}'.format(type(other)))
        return self.start_dt + timedelta(weeks=other)

    def __sub__(self, other):
        if not isinstance(other, int):
            raise ValueError('Expected integer value. Got {}'.format(type(other)))
        return self.start_dt - timedelta(weeks=other)

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