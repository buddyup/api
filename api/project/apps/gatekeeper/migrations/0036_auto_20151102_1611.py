# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations


def migrate_delete_schema(apps, schema_editor):
    from events.tasks import firebase_get, firebase_put
    pass
    # for user_id, item in firebase_get("/users", shallow=True).items():
    #     resp = firebase_get("/users/%s/buddy_requests" % user_id)
    #     print("Migrating %s" % user_id)
    #     if resp:
    #         for buddy_id, request in resp.items():
    #             firebase_put(
    #                 "/users/%s/buddies-outgoing/%s" % (buddy_id, user_id),
    #                 {".value": True}
    #             )


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0035_deleteattempt'),
    ]

    operations = [
        migrations.RunPython(migrate_delete_schema),
    ]
