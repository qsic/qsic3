import string
import urllib.request

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils import timezone

from image_cropping.fields import ImageRatioField

from py3s3.files import S3ContentFile
from qsic.parsers.improvteams.parser import ItTeamParser


class Group(models.Model):
    """
    Represents a Team or other Performance Group.
    """
    name = models.CharField(max_length=64)
    slug = models.SlugField(blank=True, default='')
    # 'it' is short for Imrpovteams / Improvteams.com
    it_url = models.URLField(null=True, blank=True)
    photo = models.ImageField(upload_to='groups/photos', null=True, blank=True)
    detail_crop = ImageRatioField('photo', '1000x800', size_warning=True)
    list_crop = ImageRatioField('photo', '970x200', size_warning=True)
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

    @property
    def is_current(self):
        gpr = GroupPerformerRelation.objects.filter(group=self)
        gpr = gpr.filter(Q(end_dt__gte=timezone.now()) | Q(end_dt=None))
        return gpr.filter(Q(start_dt__lte=timezone.now())).exists()

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super().save()

    @property
    def url(self):
        url = reverse('qsic:group_detail_view_add_slug', kwargs={'pk': self.id})
        url = ''.join((url, '/', self.slug))
        return url


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