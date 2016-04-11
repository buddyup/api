# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0026_auto_20150804_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_signed_in',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='migrated_school',
            field=models.CharField(max_length=254, blank=True, null=True),
            preserve_default=True,
        ),
    ]
