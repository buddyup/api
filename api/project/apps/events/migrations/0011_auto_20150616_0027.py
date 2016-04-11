# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20150527_1804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_timestamp',
        ),
        migrations.AddField(
            model_name='event',
            name='event_timestamp',
            field=models.DateField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
