# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0027_auto_20150807_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='migrated_first_name',
            field=models.CharField(null=True, blank=True, max_length=254),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='migrated_last_name',
            field=models.CharField(null=True, blank=True, max_length=254),
            preserve_default=True,
        ),
    ]
