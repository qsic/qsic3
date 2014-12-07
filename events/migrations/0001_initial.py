# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '__first__'),
        ('performers', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(default='', max_length=1024, blank=True)),
                ('slug', models.SlugField(default='', max_length=1024, blank=True)),
                ('_start_dt', models.DateTimeField(blank=True, null=True)),
                ('_end_dt', models.DateTimeField(blank=True, null=True)),
                ('_price', models.DecimalField(default=None, max_digits=6, decimal_places=2, blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to='events/photos', blank=True, null=True)),
                ('detail_crop', image_cropping.fields.ImageRatioField('photo', '500x500', free_crop=False, verbose_name='detail crop', hide_image_field=False, adapt_rotation=False, size_warning=True, allow_fullsize=False, help_text=None)),
                ('banner_crop', image_cropping.fields.ImageRatioField('photo', '960x300', free_crop=False, verbose_name='banner crop', hide_image_field=False, adapt_rotation=False, size_warning=True, allow_fullsize=False, help_text=None)),
                ('is_placeholder', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(default='', max_length=1024, blank=True)),
                ('slug', models.SlugField(default='', max_length=1024, blank=True)),
                ('start_dt', models.DateTimeField()),
                ('end_dt', models.DateTimeField()),
                ('price', models.DecimalField(default=None, max_digits=6, decimal_places=2, blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to='performances/photos', blank=True, null=True)),
                ('detail_crop', image_cropping.fields.ImageRatioField('photo', '500x500', free_crop=False, verbose_name='detail crop', hide_image_field=False, adapt_rotation=False, size_warning=True, allow_fullsize=False, help_text=None)),
                ('banner_crop', image_cropping.fields.ImageRatioField('photo', '960x300', free_crop=False, verbose_name='banner crop', hide_image_field=False, adapt_rotation=False, size_warning=True, allow_fullsize=False, help_text=None)),
                ('event', models.ForeignKey(to='events.Event', blank=True, null=True)),
            ],
            options={
                'ordering': ['-end_dt'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PerformanceGroupPerformerRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('group', models.ForeignKey(to='groups.Group', blank=True, null=True)),
                ('performance', models.ForeignKey(to='events.Performance')),
                ('performer', models.ForeignKey(to='performers.Performer', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReoccurringEventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=1024)),
                ('period', models.IntegerField(verbose_name='Period between events in days')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='reoccurring_event_type',
            field=models.ForeignKey(to='events.ReoccurringEventType', blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True),
            preserve_default=True,
        ),
    ]
