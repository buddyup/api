# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0034_auto_20151013_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeleteAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(null=True, auto_now_add=True)),
                ('modified_at', models.DateTimeField(null=True, auto_now=True)),
                ('attempt_full_name', models.TextField(blank=True, null=True)),
                ('attempt_email', models.TextField(blank=True, null=True)),
                ('attempt_password', models.TextField(blank=True, null=True)),
                ('attempt_terms', models.BooleanField(default=False)),
                ('attempting_ip', models.CharField(blank=True, null=True, max_length=255)),
                ('successful', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
