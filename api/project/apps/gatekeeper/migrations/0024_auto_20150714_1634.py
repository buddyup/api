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
                print("Migrating profile picture for %s" % u.buid,)
                public = firebase_get("/users/%s/public" % u.buid)
                if public and "profile_pic_url_medium" in public:
                    data = {
                        ".value": public["profile_pic_url_medium"]
                    }
                    print(data)
                    firebase_put("/users/%s/public/profile_pic" % u.buid, data)

                    if u.pic_medium:
                        firebase_put(
                            "users/%s/public/profile_pic_url_medium" % u.buid,
                            {".value": u.pic_medium.url}
                        )
                        firebase_put(
                            "users/%s/public/profile_pic_url_tiny" % u.buid,
                            {".value": u.pic_tiny.url}
                        )
                        firebase_put(
                            "users/%s/public/profile_pic" % u.buid,
                            {".value": u.pic_medium.url}
                        )
                        print("added thumbs")
                    print(".. pictures migrated.")
                else:
                    print(".. no profile found.")
        except:
            import traceback
            traceback.print_exc()


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0023_auto_20150713_1806'),
    ]

    operations = [
        migrations.RunPython(migrate_profile_pics),
    ]
