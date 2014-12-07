# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('performers', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(blank=True, default='')),
                ('it_url', models.URLField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='groups/photos')),
                ('detail_crop', image_cropping.fields.ImageRatioField('photo', '970x500', hide_image_field=False, free_crop=False, adapt_rotation=False, size_warning=True, help_text=None, allow_fullsize=False, verbose_name='detail crop')),
                ('banner_crop', image_cropping.fields.ImageRatioField('photo', '960x300', hide_image_field=False, free_crop=False, adapt_rotation=False, size_warning=True, help_text=None, allow_fullsize=False, verbose_name='banner crop')),
                ('bio', models.TextField(blank=True, null=True)),
                ('create_dt', models.DateTimeField(null=True, auto_now_add=True)),
                ('is_house_team', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupPerformerRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_dt', models.DateTimeField()),
                ('end_dt', models.DateTimeField(blank=True, null=True)),
                ('group', models.ForeignKey(to='groups.Group')),
                ('performer', models.ForeignKey(to='performers.Performer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
