# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from simplecrypt import encrypt
from binascii import hexlify
from django.conf import settings
from django.db import models, migrations
from django.db import transaction


def encrypt_logs(apps, schema_editor):
    Event = apps.get_model("events", "Event")
    # This was changed to a one-off manual command, so as not to lock the database.
    # import json
    # from binascii import hexlify
    # from simplecrypt import encrypt
    # from events.models import Event
    # from django.conf import settings

    # total = Event.objects.count()
    # c = 0
    # for e in Event.objects.all():
    #     c += 1
    #     with transaction.atomic():
    #         try:
    #             if e.data:
    #                 decoded = json.loads(e.data)
    #                 if decoded:
    #                     e.data = hexlify(encrypt(settings.ACCESS_LOG_KEY, e.data.encode('utf8')))
    #                     e.save()

    #                     e = Event.objects.get(pk=e.pk)
    #         except:
    #             import traceback
    #             traceback.print_exc()
    #             print(" -- skipping, already encrypted")
    #             pass
    #     print("%s/%s events encrypted.  (%s)" % (c, total, e.pk))


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_event_email'),
    ]

    operations = [
        migrations.RunPython(encrypt_logs),
    ]
