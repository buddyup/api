# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_emailtombstone_groupremindertombstone_pushtombstone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailtombstone',
            old_name='event',
            new_name='body',
        ),
        migrations.AddField(
            model_name='emailtombstone',
            name='email',
            field=models.CharField(max_length=50, default='', db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emailtombstone',
            name='subject',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
