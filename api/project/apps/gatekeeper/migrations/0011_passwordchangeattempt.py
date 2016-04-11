# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0010_auto_20150416_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordChangeAttempt',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(null=True, auto_now=True)),
                ('successful', models.BooleanField(default=False)),
                ('attempt_uid', models.TextField(blank=True, null=True)),
                ('attempting_ip', models.CharField(max_length=255, blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
