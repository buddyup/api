# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_profile_pics(apps, schema_editor):
    from events.tasks import firebase_get, firebase_put
    from events.handlers.events.profile import UpdateProfilePicHandler

    User = apps.get_model("gatekeeper", "User")
    for u in User.objects.all():
        try:
            if u.buid:
                print("Migrating profile picture for %s" % u.email,)
                public = firebase_get("/users/%s/public" % u.buid)
                if public:
                    firebase_put("/users/%s/pictures" % u.buid, {"original": public["profile_pic"]})
                    h = UpdateProfilePicHandler({
                        "creator": u.buid,
                    })
                    h.handle()
                    public = firebase_get("/users/%s/public" % u.buid)

                    firebase_put("/users/%s/public/profile_pic" % u.buid, {
                        ".value": public["profile_pic_url_medium"]
                    })
                    print(".. pictures migrated.")
                else:
                    print(".. no profile found.")
        except:
            import traceback
            traceback.print_exc()


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0022_auto_20150710_1914'),
    ]

    operations = [
        migrations.RunPython(migrate_profile_pics),
    ]
