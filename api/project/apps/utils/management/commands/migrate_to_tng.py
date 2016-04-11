from django.core.management.base import BaseCommand

ALL_CAMPUSES = [
    {
        "app_name": "ecampus-oregonstate-buddyup",
        "tng_id": "oregonstate_edu",
    },
    {
        "app_name": "oit-buddyup",
        "tng_id": "oit_edu",
    },
    {
        "app_name": "oregonstate-buddyup",
        "tng_id": "oregonstate_edu",
    },
    {
        "app_name": "canadacollege-buddyup",
        "tng_id": "smccd_edu",
    },
    {
        "app_name": "collegeofsanmateo-buddyup",
        "tng_id": "smccd_edu",
    },
    {
        "app_name": "skylinecollege-buddyup",
        "tng_id": "smccd_edu",
    },
    {
        "app_name": "stanford-buddyup",
        "tng_id": "stanford_edu",
    },
    {
        "app_name": "sydney-buddyup",
        "tng_id": "sydney_edu_au",
    },
    {
        "app_name": "buddyup",  # (pdx)
        "tng_id": "pdx_edu",
    },
]


class Command(BaseCommand):
    help = 'Sets up legacy apps for migration'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for c in ALL_CAMPUSES:
            print(c)
