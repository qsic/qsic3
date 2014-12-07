from django.db import models

from image_cropping.fields import ImageRatioField


class QSICPic(models.Model):
    caption = models.CharField(max_length=128, blank=True)
    photo = models.ImageField(upload_to='qsicpics/', null=True, blank=True)
    banner_crop = ImageRatioField('photo', '960x300', size_warning=True)
    event = models.ForeignKey('events.Event', null=True, blank=True)
    performance = models.ForeignKey('events.Performance', null=True, blank=True)
    group = models.ForeignKey('groups.Group', null=True, blank=True)
    performer = models.ForeignKey('performers.Performer', null=True, blank=True)

