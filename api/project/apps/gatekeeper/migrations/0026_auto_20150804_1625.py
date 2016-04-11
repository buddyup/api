# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0025_auto_20150727_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='migrated_user',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='migration_password',
            field=models.CharField(null=True, max_length=254, blank=True),
            preserve_default=True,
        ),
    ]
