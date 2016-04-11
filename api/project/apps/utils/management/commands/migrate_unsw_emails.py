import re
from django.core.management.base import BaseCommand
from gatekeeper.models import User
from gatekeeper.tasks import send_verification_email
from django.db.utils import IntegrityError


IGNORE_PREFIXES = [
    "s.yannoulatos",
    "l.hunter",
    "z5061655",
    "z5078612",
    "jacky.zhu",
    "dai.le",
    "z5019578",
    "michael.thien",
    "madeine.howard",
]


class Command(BaseCommand):
    help = 'Sets up legacy apps for migration'

    def handle(self, *args, **options):
        pattern = re.compile("^([A-z\.]+)*$")
        for u in User.objects.filter(email__icontains="unsw.edu.au", email_verified=False):

            # Emails like z5059211@unsw.edu.au should be z5059211@zmail.unsw.edu.au
            # Emails like h.low@unsw.edu.au should be h.low@student.unsw.edu.au
            # Emails like edmundlau@unsw.edu.au should be edmundlau@student.unsw.edu.au

            prefix = u.email.split("@")[0]
            domain = u.email.split("@")[1]

            if prefix not in IGNORE_PREFIXES:
                if prefix[0] == "z" and domain == "unsw.edu.au":
                    u.email = "%s@zmail.unsw.edu.au" % prefix
                    if User.objects.filter(email=u.email).count() == 0:
                        u.save()
                    else:
                        print("Account collison for %s" % u.email)
                elif pattern.match(prefix) and domain == "unsw.edu.au":
                    u.email = "%s@student.unsw.edu.au" % prefix
                    if User.objects.filter(email=u.email).count() == 0:
                        u.save()
                    else:
                        print("Account collison for %s" % u.email)
                else:
                    print("- No data change for %s" % u.email)

                send_verification_email(u.pk)
