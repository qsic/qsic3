from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from image_cropping.fields import ImageRatioField

from qsic.performers.models import Performer
from qsic.groups.models import Group


class ReoccurringEventType(models.Model):
    name = models.CharField(max_length=1024)
    period = models.IntegerField(verbose_name='Period between events in days')

    class Meta:
        app_label = 'qsic'


class Event(models.Model):
    """
    Example. QSIC House Night, QSIC Winter Ball
    """
    name = models.CharField(max_length=1024, blank=True, default='')
    slug = models.SlugField(blank=True, default='')
    # Making times and price private so that a performance(s) can
    # override them.
    _start_dt = models.DateTimeField(blank=True, null=True)
    _end_dt = models.DateTimeField(blank=True, null=True)
    _price = models.DecimalField(blank=True,
                                 null=True,
                                 max_digits=6,
                                 decimal_places=2,
                                 default=None)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='events/photos', null=True, blank=True)
    detail_crop = ImageRatioField('photo', '500x500', size_warning=True)
    banner_crop = ImageRatioField('photo', '960x300', size_warning=True)
    reoccurring_event_type = models.ForeignKey(ReoccurringEventType,
                                               null=True,
                                               blank=True)
    is_placeholder = models.BooleanField(default=False)

    class Meta:
        app_label = 'qsic'
        ordering = ['-id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.performance_offset = 0

    def __iter__(self):
        return self

    def __next__(self):
        qs = self.performance_set.order_by('start_dt')
        if self.performance_offset < qs.count():
            performance = qs[self.performance_offset]
            self.performance_offset += 1
            return performance
        else:
            self.performance_offset = 0
            raise StopIteration

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super(Event, self).save()

    def __str__(self):
        return '{} UTC {}'.format(self.start_dt.strftime('%Y-%m-%d %H:%m'), self.name)

    @property
    def start_dt(self):
        if self._start_dt:
            return self._start_dt
        elif self.performance_set.count():
            return self.performance_set.order_by('start_dt')[0].start_dt

    @property
    def end_dt(self):
        if self._end_dt:
            return self._end_dt
        elif self.performance_set.count():
            return self.performance_set.order_by('-end_dt')[0].end_dt

    @property
    def url(self):
        url = reverse('qsic:event_detial_view_add_slug', kwargs={'pk': self.id})
        url = ''.join((url, '/', self.slug))
        return url

    @property
    def type(self):
        return self.__class__.__name__

    @property
    def has_performances(self):
        return bool(self.performance_set.count())


class Performance(models.Model):
    """
    Represents a single performance. For example,
    a 20 minute set by a house night team. It could also
    be a 45 minute variety show or a two hour play.
    As long as it can not be divided into independently coherent
    pieces it can be considered a performance.
    """
    event = models.ForeignKey('qsic.Event', blank=True, null=True)
    name = models.CharField(max_length=1024, blank=True, default='')
    slug = models.SlugField(blank=True, default='')
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField()
    price = models.DecimalField(blank=True,
                                null=True,
                                max_digits=6,
                                decimal_places=2,
                                default=None)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='performances/photos', null=True, blank=True)
    detail_crop = ImageRatioField('photo', '500x500', size_warning=True)
    banner_crop = ImageRatioField('photo', '960x300', size_warning=True)

    class Meta:
        app_label = 'qsic'
        ordering = ['-end_dt']

    def __str__(self):
        return '{} {} - {}'.format(self.name, self.start_dt, self.end_dt)

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super(Performance, self).save()

    def pgpr(self):
        pgpr_set = self.performancegroupperformerrelation_set.all()
        if pgpr_set.count() != 1:
            return None
        if pgpr_set[0].group:
            return pgpr_set[0].group
        elif pgpr_set[0].performer:
            return pgpr_set[0].performer
        else:
            return None

    @property
    def url(self):
        pgpr = self.pgpr()
        if pgpr and isinstance(pgpr, Group):
            return reverse('qsic:group_detail_view_add_slug', kwargs={'pk': pgpr.id})
        elif pgpr and isinstance(pgpr, Performer):
            return reverse('qsic:performer_detail_view_add_slug', kwargs={'pk': pgpr.id})
        else:
            return '#'

    @property
    def performers(self):
        results = PerformanceGroupPerformerRelation.objects.filter(
            performance=self,
        )
        performers = []
        for result in results:
            if isinstance(result, Performer):
                performers.append(result)
            elif isinstance(result, Group):
                results = GroupPerformerRelation.objects.filter(
                    group=result,
                    start_dt__lte=datetime.now(),
                    end_dt_gte=datetime.now()
                ).select_values('performer')
                performers.extend(results)
        return performers

    @property
    def type(self):
        return self.__class__.__name__


class PerformanceGroupPerformerRelation(models.Model):
    """
    This model represents the relationhip between a performance
    and the groups or performers in participating in that performance.
    """
    performance = models.ForeignKey('qsic.Performance')
    performer = models.ForeignKey('qsic.Performer', null=True, blank=True)
    group = models.ForeignKey('qsic.Group', null=True, blank=True)

    class Meta:
        app_label = 'qsic'
