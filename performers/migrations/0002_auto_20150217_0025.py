# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('performers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performer',
            name='it_id',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
            preserve_default=True,
        ),
    ]
