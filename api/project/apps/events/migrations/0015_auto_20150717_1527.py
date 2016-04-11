# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_analytics(apps, schema_editor):
    from events.tasks import sync_analytics


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_timingtombstone'),
    ]

    operations = [
        migrations.RunPython(populate_analytics),
    ]
