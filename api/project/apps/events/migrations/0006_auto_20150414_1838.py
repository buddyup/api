# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150414_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 4, 14, 18, 38, 43, 176754)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 18, 38, 43, 176792)),
            preserve_default=True,
        ),
    ]
