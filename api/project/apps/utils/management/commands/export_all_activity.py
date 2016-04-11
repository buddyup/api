from django.core.management.base import BaseCommand
from events.models import Event
from gatekeeper.models import User

EXCLUDE_SCHOOLS = ["buddyup_org", "testcloud_io", ]


def price_data_col(e, target_type):
    if e.event_type == target_type:
        return "1"
    return ""


class Command(BaseCommand):
    help = 'Exports signups.'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        from utils.email import get_school_key_from_email
        print(
            '''"BuddyUp ID","Event Type", "buddied_up", "unbuddied", "ignored_request", ''' +
            '''"buddy_request", "cancel_buddy_request", "blocked", "unblocked", "chat_message", ''' +
            '''"report_content", "cancel_report_content", "thread_created", "private_message", ''' +
            '''"created_class", "added_class", "dropped_class", "dev_database_reset", "created_group", ''' +
            '''"updated_group", "attending_group", "cancel_group_attend", "group_reminder", "heart", ''' +
            '''"device_init", "update_profile", "account_created", "signed_up", "logged_in", ''' +
            '''"update_profile_pic", "delete_account", "page_view", "Event Date", "Email", ''' +
            '''"School ID"'''
        )

        for e in Event.objects.exclude(
            creator__contains="!!! SYSTEM!!"
        ):
            key = None
            email = e.email
            try:
                u = User.objects.get(buid=e.creator)
                key = get_school_key_from_email(u.email)
                email = u.email
            except:
                pass
            if not key:
                try:
                    key = get_school_key_from_email(e.email)
                except:
                    pass
            if key not in EXCLUDE_SCHOOLS:
                row = [
                    e.creator,
                    e.event_type,
                    price_data_col(e, "buddied_up"),
                    price_data_col(e, "unbuddied"),
                    price_data_col(e, "ignored_request"),
                    price_data_col(e, "buddy_request"),
                    price_data_col(e, "cancel_buddy_request"),
                    price_data_col(e, "blocked"),
                    price_data_col(e, "unblocked"),
                    price_data_col(e, "chat_message"),
                    price_data_col(e, "report_content"),
                    price_data_col(e, "cancel_report_content"),
                    price_data_col(e, "thread_created"),
                    price_data_col(e, "private_message"),
                    price_data_col(e, "created_class"),
                    price_data_col(e, "added_class"),
                    price_data_col(e, "dropped_class"),
                    price_data_col(e, "dev_database_reset"),
                    price_data_col(e, "created_group"),
                    price_data_col(e, "updated_group"),
                    price_data_col(e, "attending_group"),
                    price_data_col(e, "cancel_group_attend"),
                    price_data_col(e, "group_reminder"),
                    price_data_col(e, "heart"),
                    price_data_col(e, "device_init"),
                    price_data_col(e, "update_profile"),
                    price_data_col(e, "account_created"),
                    price_data_col(e, "signed_up"),
                    price_data_col(e, "logged_in"),
                    price_data_col(e, "update_profile_pic"),
                    price_data_col(e, "delete_account"),
                    price_data_col(e, "page_view"),
                    "%s" % e.created_at,
                    email,
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
