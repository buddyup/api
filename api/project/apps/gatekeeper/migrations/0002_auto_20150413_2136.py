# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 4, 13, 21, 36, 20, 540289), auto_now_add=True)),
                ('modified_at', models.DateTimeField(default=datetime.datetime(2015, 4, 13, 21, 36, 20, 540368))),
                ('successful', models.BooleanField(default=False)),
                ('attempt_email', models.TextField(null=True, blank=True)),
                ('attempt_password', models.TextField(null=True, blank=True)),
                ('attempting_ip', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 13, 21, 36, 20, 540289), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 13, 21, 36, 20, 540368)),
            preserve_default=True,
        ),
    ]
