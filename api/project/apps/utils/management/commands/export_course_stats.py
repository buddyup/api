from django.core.management.base import BaseCommand
from gatekeeper.models import User


EXCLUDE_SCHOOLS = ["buddyup_org", "testcloud_io", ]


class Command(BaseCommand):
    help = 'Prints a class breakdown'

    def handle(self, *args, **options):
        from events.tasks import firebase_get
        classes = firebase_get("/analytics/classes")

        bucket_100 = []
        bucket_200 = []
        bucket_300 = []
        bucket_400 = []
        bucket_other = []

        for _, c in classes.items():
            if c["profile"]["school_id"] not in EXCLUDE_SCHOOLS:
                code = c["profile"]["code"]
                if len(code) == 3:
                    if code[0] == "1":
                        bucket_100.append(c["code"])
                    elif code[0] == "2":
                        bucket_200.append(c["code"])
                    elif code[0] == "3":
                        bucket_300.append(c["code"])
                    elif code[0] == "4":
                        bucket_400.append(c["code"])
                    else:
                        bucket_other.append(c["code"])
                else:
                    bucket_other.append(c["code"])

        total_classes = len(classes.keys())

        print("Class Breakdown:")
        print("100-level: %s (%s%%)" % (len(bucket_100), round(100 * len(bucket_100) / total_classes, 1)))
        print("200-level: %s (%s%%)" % (len(bucket_200), round(100 * len(bucket_200) / total_classes, 1)))
        print("300-level: %s (%s%%)" % (len(bucket_300), round(100 * len(bucket_300) / total_classes, 1)))
        print("400-level: %s (%s%%)" % (len(bucket_400), round(100 * len(bucket_400) / total_classes, 1)))
        print("Other    : %s (%s%%)" % (len(bucket_other), round(100 * len(bucket_other) / total_classes, 1)))

        print("\nOthers: %s" % ",".join(bucket_other))
