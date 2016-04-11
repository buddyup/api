# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_pushtimingtombstone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtombstone',
            name='buid',
            field=models.CharField(max_length=150, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailtombstone',
            name='email',
            field=models.CharField(max_length=150, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailtombstone',
            name='event_id',
            field=models.CharField(max_length=150, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailtombstone',
            name='user_id',
            field=models.CharField(max_length=150, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='creator',
            field=models.CharField(choices=[('chat_message', 'Chat Message'), ('new_group', 'New Study Group')], blank=True, null=True, max_length=150, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='event_id',
            field=models.CharField(max_length=150, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('chat_message', 'Chat Message'), ('new_group', 'New Study Group')], blank=True, null=True, max_length=150, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='groupremindertombstone',
            name='group_id',
            field=models.CharField(max_length=150, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='groupremindertombstone',
            name='reminder_type',
            field=models.CharField(max_length=150, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pushtombstone',
            name='buid',
            field=models.CharField(max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pushtombstone',
            name='event_id',
            field=models.CharField(max_length=150, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pushtombstone',
            name='push_type',
            field=models.CharField(max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pushtombstone',
            name='user_id',
            field=models.CharField(max_length=150),
            preserve_default=True,
        ),
    ]
