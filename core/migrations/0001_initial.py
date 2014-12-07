# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '__first__'),
        ('performers', '__first__'),
        ('events', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='QSICPic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('caption', models.CharField(max_length=128, blank=True)),
                ('photo', models.ImageField(upload_to='qsicpics/', blank=True, null=True)),
                ('banner_crop', image_cropping.fields.ImageRatioField('photo', '960x300', allow_fullsize=False, size_warning=True, free_crop=False, help_text=None, hide_image_field=False, verbose_name='banner crop', adapt_rotation=False)),
                ('event', models.ForeignKey(to='events.Event', null=True, blank=True)),
                ('group', models.ForeignKey(to='groups.Group', null=True, blank=True)),
                ('performance', models.ForeignKey(to='events.Performance', null=True, blank=True)),
                ('performer', models.ForeignKey(to='performers.Performer', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
