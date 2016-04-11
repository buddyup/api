# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 4, 13, 20, 22, 35, 282912), auto_now_add=True)),
                ('modified_at', models.DateTimeField(default=datetime.datetime(2015, 4, 13, 20, 22, 35, 282974))),
                ('event_type', models.CharField(max_length=50, choices=[('chat_message', 'Chat Message'), ('new_group', 'New Study Group')])),
                ('event_data', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
