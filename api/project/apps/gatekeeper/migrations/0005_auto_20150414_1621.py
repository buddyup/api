# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


default_emails = [
    "steven@buddyup.org",
    "brian@buddyup.org",
    "john@buddyup.org",
]


def add_default_users(apps, schema_editor):

    User = apps.get_model("gatekeeper", "User")
    # for e in default_emails:
    #     assert User.objects.filter(email=e).count() == 0
    #     u = User.objects.create(
    #         email=e,
    #         password="pbkdf2_sha256$15000$RxYLEtuTfftf$jocf8DNOZID7Eze/IhTZUgtiXMDEioiHD6alFUASl0c=",
    #         must_reset_password=True,
    #     )


def remove_default_users(apps, schema_editor):
    User = apps.get_model("gatekeeper", "User")
    for e in default_emails:
        User.objects.filter(email=e).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0004_auto_20150414_1619'),
    ]

    operations = [
        migrations.RunPython(add_default_users, remove_default_users)
    ]
