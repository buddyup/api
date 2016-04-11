import datetime
import time

from django.core.management.base import BaseCommand
from gatekeeper.models import User
from events.handlers.events.dev_database_reset import DevDatabaseResetHandler


class Command(BaseCommand):
    help = 'Imports all schools, based on our sources.'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        from django.conf import settings
        settings.CELERY_ALWAYS_EAGER = True

        default_emails = [
            "steven@buddyup.org",
            "brian@buddyup.org",
            "john@buddyup.org",
            "hiliary@buddyup.org",
        ]

        for e in default_emails:
            if User.objects.filter(email=e).count() == 0:
                print("Added %s" % e)
                User.objects.create(
                    email=e,
                    password="pbkdf2_sha256$15000$RxYLEtuTfftf$jocf8DNOZID7Eze/IhTZUgtiXMDEioiHD6alFUASl0c=",
                    must_reset_password=True,
                    email_verified=True,
                    staff_flag=True
                )
            else:
                u = User.objects.get(email=e)
                u.email_verified = True
                u.staff_flag = True
                u.save()

        now = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
        d = DevDatabaseResetHandler({
            "created_at": now
        })
        d.handle()
        print("Reset Firebase.")
