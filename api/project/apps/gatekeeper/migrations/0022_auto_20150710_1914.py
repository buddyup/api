# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0021_auto_20150618_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pic_medium',
            field=models.ImageField(blank=True, upload_to='profile_pics', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='pic_original',
            field=models.ImageField(blank=True, upload_to='profile_pics', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='pic_tiny',
            field=models.ImageField(blank=True, upload_to='profile_pics', null=True),
            preserve_default=True,
        ),
    ]
