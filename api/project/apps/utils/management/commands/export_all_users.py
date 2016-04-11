from django.core.management.base import BaseCommand
from gatekeeper.models import User


EXCLUDE_SCHOOLS = ["buddyup_org", "testcloud_io", ]


class Command(BaseCommand):
    help = 'Exports emails for campaigns - temp fix.'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        from utils.email import get_school_key_from_email
        print(
            '"BuddyUp ID", "Email", "First name", "Last name", "School",' +
            ' "Was Migrated", "Temp password", "Has signed in", "Created On", "Total Event Count",' +
            ' "Number of Classes"'
        )

        for u in User.objects.all():
            key = get_school_key_from_email(u.email)

            if key not in EXCLUDE_SCHOOLS:
                row = [
                    u.buid,
                    u.email,
                    u.migrated_first_name,
                    u.migrated_last_name,
                    key,
                    u.migrated_user,
                    u.migration_password,
                    u.has_signed_in,
                    ("%s" % u.created_at).split(" ")[0],
                    # Disabled for now.
                    # u.total_events,
                    # u.total_classes,
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
