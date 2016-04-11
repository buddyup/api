# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0016_signupattempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordchangeattempt',
            name='attempt_buid',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
