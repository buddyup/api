# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0006_auto_20150414_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginattempt',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 16, 0, 15, 54, 679062), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='loginattempt',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 16, 0, 15, 54, 679342)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 16, 0, 15, 54, 679062), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(db_index=True, max_length=254, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 16, 0, 15, 54, 679342)),
            preserve_default=True,
        ),
    ]
