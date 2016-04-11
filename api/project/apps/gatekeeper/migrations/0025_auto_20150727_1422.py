# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_buid_to_public(apps, schema_editor):
    from events.tasks import firebase_put

    User = apps.get_model("gatekeeper", "User")
    for u in User.objects.all():
        try:
            if u.buid:
                print(u.email)
                firebase_put("/users/%s/public/buid" % u.buid, {".value": u.buid})
        except:
            import traceback
            traceback.print_exc()


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0024_auto_20150714_1634'),
    ]

    operations = [
        migrations.RunPython(add_buid_to_public),
    ]
