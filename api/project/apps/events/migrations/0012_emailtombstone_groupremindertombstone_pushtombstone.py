# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20150616_0027'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTombstone',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(null=True, auto_now_add=True)),
                ('modified_at', models.DateTimeField(null=True, auto_now=True)),
                ('user_id', models.CharField(db_index=True, max_length=50)),
                ('buid', models.CharField(db_index=True, max_length=50)),
                ('event_id', models.CharField(db_index=True, max_length=50)),
                ('event', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupReminderTombstone',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(null=True, auto_now_add=True)),
                ('modified_at', models.DateTimeField(null=True, auto_now=True)),
                ('group_id', models.CharField(db_index=True, max_length=50)),
                ('reminder_type', models.CharField(db_index=True, max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PushTombstone',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(null=True, auto_now_add=True)),
                ('modified_at', models.DateTimeField(null=True, auto_now=True)),
                ('push_type', models.CharField(max_length=50)),
                ('user_id', models.CharField(max_length=50)),
                ('buid', models.CharField(max_length=50)),
                ('event_id', models.CharField(db_index=True, max_length=50)),
                ('tokens', models.TextField(blank=True, null=True)),
                ('event', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
