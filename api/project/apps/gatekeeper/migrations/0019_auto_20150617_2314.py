# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def default_buids(apps, schema_editor):
    user_model = apps.get_model("gatekeeper", "User")
    for user in user_model.objects.all():
        user.buid = "user-%s" % (user.pk,)
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0018_user_buid'),
    ]

    operations = [
        migrations.RunPython(default_buids),
    ]
