# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_apitimingtombstone'),
    ]

    operations = [
        migrations.AddField(
            model_name='apitimingtombstone',
            name='success',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
