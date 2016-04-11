# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_auto_20151013_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='email',
            field=models.CharField(max_length=150, db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
