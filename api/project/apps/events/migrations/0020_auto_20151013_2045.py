# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_auto_20151012_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_timestamp',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
