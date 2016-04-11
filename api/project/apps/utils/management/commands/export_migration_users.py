from django.core.management.base import BaseCommand
from gatekeeper.models import User


class Command(BaseCommand):
    help = 'Sets up legacy apps for migration'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        print('"Email", "First name", "Last name", "School", "Temp password", "Has signed in"')

        for u in User.objects.filter(migrated_user=True):
            row = [
                u.email,
                u.migrated_first_name,
                u.migrated_last_name,
                u.migrated_school,
                u.migration_password,
                u.has_signed_in,
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
