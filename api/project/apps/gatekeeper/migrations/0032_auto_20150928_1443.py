# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_emails(apps, schema_editor):
    from events.tasks import firebase_patch

    User = apps.get_model("gatekeeper", "User")
    for u in User.objects.all():
        print("migrating %s" % u.email)
        try:
            if u.buid:
                firebase_patch("/users/%s/private/" % u.buid, {
                    "email": u.email,
                })
        except:
            import traceback
            traceback.print_exc()


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0031_auto_20150922_2108'),
    ]

    operations = [
        migrations.RunPython(migrate_emails),
    ]
