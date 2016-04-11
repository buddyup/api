# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import random

from django.db import models, migrations


def default_email_keys(apps, schema_editor):
    user_model = apps.get_model("gatekeeper", "User")
    for user in user_model.objects.all():
        salt = hashlib.sha1(str(random.random()).encode("utf-8")).hexdigest()[:5]
        user.email_confirm_key = hashlib.sha1(salt.encode("utf-8") + user.email.encode("utf-8")).hexdigest()
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0020_user_email_confirm_key'),
    ]

    operations = [
        migrations.RunPython(default_email_keys),
    ]
