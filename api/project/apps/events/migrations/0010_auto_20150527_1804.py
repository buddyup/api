# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20150416_0025'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_data',
            new_name='data',
        ),
        migrations.AddField(
            model_name='event',
            name='creator',
            field=models.CharField(max_length=50, null=True, db_index=True, blank=True, choices=[('chat_message', 'Chat Message'), ('new_group', 'New Study Group')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='event_id',
            field=models.CharField(max_length=50, db_index=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='event_timestamp',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(max_length=50, null=True, db_index=True, blank=True, choices=[('chat_message', 'Chat Message'), ('new_group', 'New Study Group')]),
            preserve_default=True,
        ),
    ]
