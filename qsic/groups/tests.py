from datetime import datetime

from django.test import TestCase
from django.utils.timezone import utc

from freezegun import freeze_time

from qsic.groups.models import Group
from qsic.groups.models import GroupPerformerRelation
from qsic.performers.models import Performer


class PerformerInGroupIteratorTC(TestCase):
    """
    A Test Case to assert the behavior of the group iterator.
    """
    def setUp(self):
        # A group with one Performer
        self.g1 = Group.objects.create(
            name='House Party!',
            create_dt=datetime(2014, 1, 1, tzinfo=utc)
        )
        self.p1 = Performer.objects.create(first_name='Nathan', last_name='Phillips')
        GroupPerformerRelation.objects.create(
            group=self.g1,
            performer=self.p1,
            start_dt=datetime(2014, 1, 1, tzinfo=utc),
            end_dt=datetime(2014, 2, 1, tzinfo=utc)
        )

        # A group with 3 performers, 1 of which left the group 2 weeks after starting.
        self.g2 = Group.objects.create(
            name='Block Party!',
            create_dt=datetime(2014, 1, 15, tzinfo=utc)
        )
        self.p2 = Performer.objects.create(first_name='Morgan', last_name='James')
        self.p3 = Performer.objects.create(first_name='Micheal', last_name='Phelps')
        self.p4 = Performer.objects.create(first_name='Cindy', last_name='Luhoo')
        GroupPerformerRelation.objects.create(
            group=self.g2,
            performer=self.p2,
            start_dt=datetime(2014, 1, 15, tzinfo=utc),
        )
        GroupPerformerRelation.objects.create(
            group=self.g2,
            performer=self.p3,
            start_dt=datetime(2014, 1, 15, tzinfo=utc),
        )
        GroupPerformerRelation.objects.create(
            group=self.g2,
            performer=self.p4,
            start_dt=datetime(2014, 1, 15, tzinfo=utc),
            end_dt=datetime(2014, 2, 1, tzinfo=utc)
        )

    @freeze_time("2014-01-12 00:00:00", tz_offset=0)
    def test_group_with_one_peformer(self):
        self.assertEqual(len([p for p in self.g1]), 1)

    @freeze_time("2014-02-12 00:00:00", tz_offset=0)
    def test_group_with_no_performers_after_last_performer_end_dt(self):
        self.assertEqual(len([p for p in self.g1]), 0)

    @freeze_time("2014-02-12 00:00:00", tz_offset=0)
    def test_group_with_three_performers_two_active(self):
        self.assertEqual(len([p for p in self.g2]), 2)