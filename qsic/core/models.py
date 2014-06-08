from django.db import models

from image_cropping.fields import ImageRatioField


class QSICPic(models.Model):
    caption = models.CharField(max_length=128, blank=True)
    photo = models.ImageField(upload_to='qsicpics/', null=True, blank=True)
    banner_crop = ImageRatioField('photo', '970x200', size_warning=True)
    event = models.ForeignKey('qsic.Event', null=True, blank=True)
    performance = models.ForeignKey('qsic.Performance', null=True, blank=True)
    group = models.ForeignKey('qsic.Group', null=True, blank=True)
    performer = models.ForeignKey('qsic.Performer', null=True, blank=True)

    class Meta:
        app_label = 'qsic'
