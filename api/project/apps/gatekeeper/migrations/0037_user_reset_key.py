# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0036_auto_20151102_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reset_key',
            field=models.CharField(max_length=512, blank=True, unique=True, null=True, db_index=True),
            preserve_default=True,
        ),
    ]
