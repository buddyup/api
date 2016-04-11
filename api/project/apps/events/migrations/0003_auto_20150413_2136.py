# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150413_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 13, 21, 36, 20, 540289), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 13, 21, 36, 20, 540368)),
            preserve_default=True,
        ),
    ]
