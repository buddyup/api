# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0003_auto_20150413_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='must_reset_password',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='loginattempt',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 16, 19, 19, 973718), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='loginattempt',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 16, 19, 19, 973762)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 16, 19, 19, 973718), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 16, 19, 19, 973762)),
            preserve_default=True,
        ),
    ]
