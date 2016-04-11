from django.core.management.base import BaseCommand
from events.models import Event


class Command(BaseCommand):
    help = 'Exports signups.'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        from utils.email import get_school_key_from_email
        print('"BuddyUp ID", "Signup Date", "Email", "School ID"')

        for e in Event.objects.filter(event_type="signed_up"):
            key = None
            try:
                key = get_school_key_from_email(e.email)
            except:
                pass
            row = [
                e.creator,
                e.event_timestamp,
                e.email,
                key,
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
