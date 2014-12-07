from datetime import datetime

from django.test import TestCase
from django.utils.timezone import utc

from freezegun import freeze_time

from groups.models import Group
from groups.models import GroupPerformerRelation
from performers.models import Performer


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


class SlugTC(TestCase):
    """
    A test case for all slug related tests.
    """
    def test_save_group_generates_correct_slug(self):
        g = Group.objects.create(name='Mc.Sorelys Party Time')
        self.assertEqual(g.slug, 'mcsorelys-party-time')

    def test_get_group_detail_view_redirects_to_view_with_slug(self):
        g = Group.objects.create(name='+++Butter High++')
        response = self.client.get('/groups/group/' + str(g.id), follow=True)
        self.assertTrue(hasattr(response, 'request'))
        self.assertEqual(response.request['PATH_INFO'], g.url)


class IsCurrentTC(TestCase):
    """
    Test ``is_current`` method on Group model.
    """
    def setUp(self):
        self.g = Group.objects.create(
            name='House Party!',
            create_dt=datetime(2014, 1, 1, tzinfo=utc)
        )
        self.p1 = Performer.objects.create(first_name='Nathan', last_name='Phillips')
        self.p2 = Performer.objects.create(first_name='Morgan', last_name='James')
        self.gpr1 = GroupPerformerRelation.objects.create(
            group=self.g,
            performer=self.p1,
            start_dt=datetime(2014, 1, 1, tzinfo=utc),
            end_dt=datetime(2014, 2, 1, tzinfo=utc)
        )
        self.gpr2 = GroupPerformerRelation.objects.create(
            group=self.g,
            performer=self.p2,
            start_dt=datetime(2014, 1, 15, tzinfo=utc),
        )

    @freeze_time("2013-12-12 00:00:00", tz_offset=0)
    def test_group_not_current_before_first_member_joins(self):
        self.assertFalse(self.g.is_current)

    @freeze_time("2014-01-10 00:00:00", tz_offset=0)
    def test_group_is_current_when_one_member_joins(self):
        self.assertTrue(self.g.is_current)

    @freeze_time("2014-01-20 00:00:00", tz_offset=0)
    def test_group_is_current_when_no_member_has_end_dt(self):
        self.assertTrue(self.g.is_current)

    @freeze_time("2014-02-20 00:00:00", tz_offset=0)
    def test_group_is_current_when_no_member_has_end_dt(self):
        self.gpr2.end_dt = datetime(2014, 2, 15, tzinfo=utc)
        self.gpr2.save()
        self.assertFalse(self.g.is_current)