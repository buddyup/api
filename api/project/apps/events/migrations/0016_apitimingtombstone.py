# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20150717_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='APITimingTombstone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(null=True, auto_now_add=True)),
                ('modified_at', models.DateTimeField(null=True, auto_now=True)),
                ('response_time', models.FloatField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
