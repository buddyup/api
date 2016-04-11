# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0011_passwordchangeattempt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='api_jwt_cached',
            field=models.CharField(blank=True, max_length=512, unique=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='fire_jwt_cached',
            field=models.CharField(blank=True, max_length=512, unique=True, null=True),
            preserve_default=True,
        ),
    ]
