from django.db import models

from qsic.performers.models import Performer
from qsic.groups.models import Group


class EventSeries(models.Model):
    """
    Exmaple: QSIC House Nights as a whole, QSIC Saturday Musical Nights
    """
    name = models.CharField(max_length=1024, blank=True, default='')
    description = models.TextField(blank=True)

    class Meta:
        app_label = 'qsic'
        ordering = ['-id']

    def __str__(self):
        return '{}'.format(self.name)


class Event(models.Model):
    """
    Example. QSIC House Night, QSIC Winter Ball
    """
    event_series = models.ForeignKey('qsic.EventSeries', blank=True, null=True)
    name = models.CharField(max_length=1024, blank=True, default='')
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

    class Meta:
        app_label = 'qsic'
        ordering = ['-id']

    def __str__(self):
        return 'Event {}'.format(self.name)

    @property
    def start_dt(self):
        if self._start_dt:
            return _start_dt
        elif self.performance_set.count():
            return self.performance_set.order_by('start_dt')[0]


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
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField()
    price = models.DecimalField(blank=True,
                                null=True,
                                max_digits=6,
                                decimal_places=2,
                                default=None)

    class Meta:
        app_label = 'qsic'
        ordering = ['-end_dt']

    def __str__(self):
        return 'Performance {} {} - {}'.format(self.name, self.start_dt, self.end_dt)

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
