# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 4, 13, 20, 23, 5, 554538))),
                ('modified_at', models.DateTimeField(default=datetime.datetime(2015, 4, 13, 20, 23, 5, 554589))),
                ('email', models.CharField(max_length=254, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
