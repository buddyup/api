# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0009_auto_20150416_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='api_jwt_cached',
            field=models.CharField(null=True, max_length=255, blank=True, unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='fire_jwt_cached',
            field=models.CharField(null=True, max_length=255, blank=True, unique=True),
            preserve_default=True,
        ),
    ]
