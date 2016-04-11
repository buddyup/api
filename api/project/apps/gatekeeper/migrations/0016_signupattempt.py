# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0015_user_agreed_to_terms'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignupAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(null=True, auto_now_add=True)),
                ('modified_at', models.DateTimeField(null=True, auto_now=True)),
                ('attempt_full_name', models.TextField(null=True, blank=True)),
                ('attempt_email', models.TextField(null=True, blank=True)),
                ('attempt_password', models.TextField(null=True, blank=True)),
                ('attempt_terms', models.BooleanField(default=False)),
                ('attempting_ip', models.CharField(null=True, max_length=255, blank=True)),
                ('successful', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
