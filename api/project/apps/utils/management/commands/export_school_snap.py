from django.core.management.base import BaseCommand
from gatekeeper.models import User


class Command(BaseCommand):
    help = 'Exports list of students w/ class number and buddy number - temp fix.'

    def add_arguments(self, parser):
        parser.add_argument('school', nargs='+', type=int)

    def handle(self, *args, **options):
        from utils.email import get_school_key_from_email
        from events.tasks import firebase_get, firebase_put

        print(
            '"BuddyUp ID", "Email", "Num Classes", "Num Buddies"'
        )

        users = User.objects.all()

        if len(args):
            users = users.filter(email__icontains=args[0])
        for u in users:

            classes = firebase_get("/users/%s/classes" % u.buid, shallow=True)
            buddies = firebase_get("/users/%s/buddies" % u.buid, shallow=True)

            num_classes = 0
            num_buddies = 0
            if classes:
                num_classes = len(classes.keys())
            if buddies:
                num_buddies = len(buddies.keys())

            row = [
                u.buid,
                u.email,
                num_classes,
                num_buddies,
            ]
            row_str = ""
            for r in row:
                if r is None:
                    r_str = ""
                elif r is False:
                    r_str = "false"
                elif r is True:
                    r_str = "true"
                else:
                    r_str = "%s" % r
                    r_str = r_str.replace(",", "\,")

                row_str = row_str + "%s," % r_str

            row_str = row_str[:-1]

            print(row_str)
