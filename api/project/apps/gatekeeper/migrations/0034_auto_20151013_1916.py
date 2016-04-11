# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from utils.email import get_school_key_from_email


def add_school(apps, schema_editor):

    User = apps.get_model("gatekeeper", "User")
    for u in User.objects.all():
        if u.email and "@" in u.email:
            u.main_school = get_school_key_from_email(u.email)
            u.save()


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0033_user_main_school'),
    ]

    operations = [
        migrations.RunPython(add_school)
    ]
