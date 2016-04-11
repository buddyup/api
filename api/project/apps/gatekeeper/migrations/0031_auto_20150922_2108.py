# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models, migrations


def fix_profile_pics(apps, schema_editor):
    from events.tasks import firebase_get, firebase_put
    from events.handlers.events.profile import UpdateProfilePicHandler

    bug_start_date = datetime.date(year=2015, day=1, month=9)
    print(bug_start_date)

    User = apps.get_model("gatekeeper", "User")
    for u in User.objects.filter(created_at__gt=bug_start_date):
        try:
            if u.buid:
                print("Migrating profile picture for %s" % u.email,)
                print("Migrating profile picture for %s" % u.buid,)

                h = UpdateProfilePicHandler({
                    "creator": u.buid,
                })
                h.handle()
                public = firebase_get("/users/%s/public" % u.buid)

                firebase_put("/users/%s/public/profile_pic" % u.buid, {
                    ".value": public["profile_pic_url_medium"]
                })
                print(".. pictures migrated.")
        except:
            import traceback
            traceback.print_exc()


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0030_auto_20150910_1453'),
    ]

    operations = [
        migrations.RunPython(fix_profile_pics),
    ]
