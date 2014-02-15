import string
import urllib.request

from django.db import models
from django.db.models import Q
from django.utils import timezone

from py3s3.files import S3ContentFile
from qsic.parsers.improvteams.parser import ItTeamParser


class Group(models.Model):
    """
    Represents a Team or other Performance Group.
    """
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)
    # 'it' is short for Imrpovteams / Improvteams.com
    it_url = models.URLField(null=True, blank=True)
    photo = models.ImageField(upload_to='performers/headshots',
                              null=True,
                              blank=True)
    bio = models.TextField(null=True, blank=True)
    create_dt = models.DateTimeField(auto_now_add=True, null=True)
    is_house_team = models.BooleanField(default=True)

    class Meta:
        app_label = 'qsic'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.performer_offset = 0

    def __str__(self):
        return self.name

    def __iter__(self):
        return self

    def __next__(self):
        qs = self.groupperformerrelation_set.all()
        qs = qs.filter(
            Q(start_dt__lte=timezone.now()),
            Q(end_dt__gte=timezone.now()) | Q(end_dt=None)
        )

        if self.performer_offset < qs.count():
            performer = qs[self.performer_offset]
            self.performer_offset += 1
            return performer
        else:
            raise StopIteration

    # TODO test this method
    @property
    def is_current(self):
        return GroupPerformerRelation.objects.filter(group=self).filter(
            Q(start_dt__lte=timezone.now()),
            (Q(end_dt__gte=timezone.now() | Q(end_dt=None)))
        ).exists()


class GroupPerformerRelation(models.Model):
    """
    This model represents the relationship between a performer and a
    performance group. A performer is always part of a group. Whether the
    performer appears on a team's current roster depends on if the peroformer
    has a ``GroupPerfromerRelation`` for the group.
    """
    group = models.ForeignKey('qsic.Group')
    performer = models.ForeignKey('qsic.Performer')

    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'qsic'

    def __str__(self):
        return '{} in {}'.format(self.performer, self.group)