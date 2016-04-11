# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0014_auto_20150601_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='agreed_to_terms',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='passwordchangeattempt',
            name='attempt_uid',
        ),
    ]
