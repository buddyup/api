# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0002_auto_20150413_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginattempt',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 13, 21, 49, 11, 799061), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='loginattempt',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 13, 21, 49, 11, 799114)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 13, 21, 49, 11, 799061), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 13, 21, 49, 11, 799114)),
            preserve_default=True,
        ),
    ]
