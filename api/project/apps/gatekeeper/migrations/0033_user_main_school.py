# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0032_auto_20150928_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='main_school',
            field=models.CharField(null=True, blank=True, max_length=512, db_index=True),
            preserve_default=True,
        ),
    ]
