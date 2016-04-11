# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0017_auto_20150609_0223'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='buid',
            field=models.CharField(max_length=512, db_index=True, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
