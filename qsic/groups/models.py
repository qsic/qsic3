import urllib.request

from django.db import models

from py3s3.files import S3ContentFile
from qsic.parsers.improvteams.parser import ItTeamParser


class Group(models.Model):
    """
    Represents a Team or other Performance Group.
    """
    name = models.CharField(max_length=64)
    # 'it' is short for Imrpovteams / Improvteams.com
    it_url = models.URLField(null=True, blank=True)
    photo = models.ImageField(upload_to='performers/headshots',
                              null=True,
                              blank=True)
    bio = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'qsic'


class GroupPerformerRelation(models.Model):
    """
    This model represents the relationship between a play and a
    performance group. A performer can be on a team from
    start dt to end dt.
    """
    group = models.ForeignKey('qsic.Group')
    performer = models.ForeignKey('qsic.Performer')

    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField()

    class Meta:
        app_label = 'qsic'