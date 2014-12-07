# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Performer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('slug', models.SlugField(default='', blank=True)),
                ('it_url', models.URLField(blank=True, null=True)),
                ('it_id', models.PositiveIntegerField(blank=True, null=True)),
                ('photo', models.ImageField(upload_to='performers/photos', blank=True, null=True)),
                ('detail_crop', image_cropping.fields.ImageRatioField('photo', '300x300', adapt_rotation=False, hide_image_field=False, allow_fullsize=False, verbose_name='detail crop', free_crop=False, help_text=None, size_warning=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
