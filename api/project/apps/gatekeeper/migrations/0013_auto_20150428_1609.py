# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0012_auto_20150417_0053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passwordchangeattempt',
            old_name='attempt_uid',
            new_name='attempt_uid',
        ),
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='staff_flag',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
