# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0019_auto_20150617_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_confirm_key',
            field=models.CharField(unique=True, null=True, db_index=True, blank=True, max_length=512),
            preserve_default=True,
        ),
    ]
