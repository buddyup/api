import sys
import datetime
import json
from django.core.management.base import BaseCommand
from events.models import Event
from gatekeeper.models import User
from binascii import hexlify, unhexlify
from simplecrypt import encrypt, decrypt
from django.conf import settings


class Course(object):

    def __init__(self, school_id, subject_code, code):
        self.school_id = school_id
        self.subject_code = subject_code
        self.code = code


EXCLUDE_SCHOOLS = ["buddyup_org", "testcloud_io", ]


# - University of Oregon (CH 221, MATH 241, CH 227, SOC 204, MATH 111)
# - University of Washington (BIO 180, CH 237)
# - Portland State (IT 101, CS 162, MTH 251)
INCLUDE_CLASSES = []
INCLUDE_CLASSES.append(Course("uoregon_edu", "CH", "221"))
INCLUDE_CLASSES.append(Course("uoregon_edu", "MATH", "241"))
INCLUDE_CLASSES.append(Course("uoregon_edu", "CH", "227"))
INCLUDE_CLASSES.append(Course("uoregon_edu", "SOC", "204"))
INCLUDE_CLASSES.append(Course("uoregon_edu", "MATH", "111"))
INCLUDE_CLASSES.append(Course("washington_edu", "BIO", "180"))
INCLUDE_CLASSES.append(Course("washington_edu", "CHEM", "237"))
INCLUDE_CLASSES.append(Course("pdx_edu", "IT", "101"))
INCLUDE_CLASSES.append(Course("pdx_edu", "CS", "162"))
INCLUDE_CLASSES.append(Course("pdx_edu", "MTH", "251"))


class Command(BaseCommand):
    help = 'Exports dense pilots vs everyone.'

    def handle(self, *args, **options):
        # - Total Users in Sample? 2,000-ish?
        # - Average Opens per Week (Break-down First 6 weeks vs.
            # Second 6 weeks and First 6 weeks of Subsequent Term if possible),
        # - Buddy-per-user Ratio, (or something in the spirit of “the average user in this sample made X# of buddies”),
        # - Number of Users in sample who Opened the App more than 25 times
            # (or “power users”) unless you want to make up a different definition of power user (e.g. has 3+ buddies).

        # - Average days of use.
        # - 1-1 messages per user

        # TODO: we don't double-count buddies, but we should.
        # total_users = User.objects.count()
        excluded_users = 0

        in_total_users = 0
        in_events_total = 0
        in_opens_per_week = 0
        in_buddies = 0
        in_buddy_requests_sent = 0
        in_days_of_use = 0
        in_one_to_one_messages = 0

        out_total_users = 0
        out_events_total = 0
        out_opens_per_week = 0
        out_buddies = 0
        out_buddy_requests_sent = 0
        out_days_of_use = 0
        out_one_to_one_messages = 0

        bio180_total_users = 0
        bio180_events_total = 0
        bio180_opens_per_week = 0
        bio180_buddies = 0
        bio180_buddy_requests_sent = 0
        bio180_days_of_use = 0
        bio180_one_to_one_messages = 0

        window_start_date = datetime.date(year=2015, day=15, month=9)
        window_end_date = datetime.date(year=2015, day=15, month=12)

        for u in User.objects.all():
            in_cohort = False
            in_bio_180 = False
            skip_user = False
            one_class_decrypted = False
            for e in Event.objects.filter(
                event_timestamp__gte=window_start_date,
                event_timestamp__lte=window_end_date,
                creator=u.buid, event_type="added_class"
            ):
                try:
                    # data_str = hexlify(decrypt(settings.ACCESS_LOG_KEY, e.data.encode('utf8')))
                    data_str = decrypt(settings.ACCESS_LOG_KEY, unhexlify(e.data)).decode('utf8')
                    data = json.loads(data_str)
                    one_class_decrypted = True
                    if data["school_id"] in EXCLUDE_SCHOOLS:
                        skip_user = True
                        break

                    for c in INCLUDE_CLASSES:
                        #   "id": course.id,
                        # "course_id": course.id,
                        # "name": course.name,
                        # "code": course.code,
                        # "school_id": course.school_id,
                        # "subject_code": course.subject_code,
                        # "subject_name": course.subject_name,
                        # "subject_icon": course.subject_icon,
                        if (
                            data["school_id"] == c.school_id and
                            data["subject_code"] == c.subject_code and
                            data["code"] == c.code
                        ):
                            in_cohort = True

                            if data["code"] == "180":
                                in_bio_180 = True

                except:
                    pass

            if one_class_decrypted and not skip_user and Event.objects.filter(
                event_timestamp__gte=window_start_date,
                event_timestamp__lte=window_end_date,
                creator=u.buid
            ).count() > 1:
                first_event = Event.objects.filter(
                    event_timestamp__gte=window_start_date,
                    event_timestamp__lte=window_end_date,
                    creator=u.buid
                ).order_by("event_timestamp")[0]
                last_event = Event.objects.filter(
                    event_timestamp__gte=window_start_date,
                    event_timestamp__lte=window_end_date,
                    creator=u.buid
                ).order_by("-event_timestamp")[0]
                diff = last_event.event_timestamp - first_event.event_timestamp
                num_days_used = diff.total_seconds() / 60 / 60 / 24

                # Num opens
                events = Event.objects.filter(
                    event_timestamp__gte=window_start_date,
                    event_timestamp__lte=window_end_date,
                    creator=u.buid
                ).order_by("event_timestamp").all()
                last_e = events[0]
                num_opens = 0
                for e in events:
                    if e.creator:
                        if (
                            not last_e or
                            last_e.creator != e.creator or
                            (e.event_timestamp - last_e.event_timestamp).total_seconds() >= 60
                        ):
                            num_opens += 1
                            last_e = e

                num_unbuddied = Event.objects.filter(
                    event_timestamp__gte=window_start_date,
                    event_timestamp__lte=window_end_date,
                    creator=u.buid, event_type="unbuddied"
                ).count()
                num_buddy_request = Event.objects.filter(
                    event_timestamp__gte=window_start_date,
                    event_timestamp__lte=window_end_date,
                    creator=u.buid, event_type="buddy_request"
                ).count()
                num_buddied_up = Event.objects.filter(
                    event_timestamp__gte=window_start_date,
                    event_timestamp__lte=window_end_date,
                    creator=u.buid, event_type="buddied_up"
                ).count()
                num_buddies = num_buddied_up - num_unbuddied
                num_one_to_one = Event.objects.filter(
                    event_timestamp__gte=window_start_date,
                    event_timestamp__lte=window_end_date,
                    creator=u.buid, event_type="private_message"
                ).count()
                num_events = Event.objects.filter(
                    event_timestamp__gte=window_start_date,
                    event_timestamp__lte=window_end_date,
                    creator=u.buid
                ).count()

                if in_cohort:
                    in_total_users += 1
                    in_events_total += num_events
                    in_opens_per_week += num_opens
                    in_buddies += num_buddies
                    in_buddy_requests_sent += num_buddy_request
                    in_days_of_use += num_days_used
                    in_one_to_one_messages += num_one_to_one
                    print('*', end="", flush=True)
                else:
                    out_total_users += 1
                    out_events_total += num_events
                    out_opens_per_week += num_opens
                    out_buddies += num_buddies
                    out_buddy_requests_sent += num_buddy_request
                    out_days_of_use += num_days_used
                    out_one_to_one_messages += num_one_to_one
                    print('.', end="", flush=True)

                if in_bio_180:
                    bio180_total_users += 1
                    bio180_events_total += num_events
                    bio180_opens_per_week += num_opens
                    bio180_buddies += num_buddies
                    bio180_buddy_requests_sent += num_buddy_request
                    bio180_days_of_use += num_days_used
                    bio180_one_to_one_messages += num_one_to_one

            else:
                print('x', end="", flush=True)
                excluded_users += 1

            sys.stdout.flush()

        print("%s excluded" % excluded_users)
        print("")
        print("Cohort Analysis")
        print("")
        print("          In Critical Mass Cohort  |  Other Users  | Bio180")
        print("Students             %s                     %s" % (in_total_users, out_total_users))
        print("Events/User          %.2f                     %.2f             %.2f" % (
            in_events_total / in_total_users, out_events_total / out_total_users, bio180_events_total / bio180_total_users,)
        )
        print("Opens/Wk/User        %.2f                     %.2f             %.2f" % (
            in_opens_per_week / in_total_users, out_opens_per_week / out_total_users, bio180_opens_per_week / bio180_total_users,)
        )
        print("Buddies/User         %.2f                     %.2f             %.2f" % (
            in_buddies / in_total_users, out_buddies / out_total_users, bio180_buddies / bio180_total_users,)
        )
        print("Buddy Requests/User  %.2f                     %.2f             %.2f" % (
            in_buddy_requests_sent / in_total_users,
            out_buddy_requests_sent / out_total_users,
            bio180_buddy_requests_sent / bio180_total_users,
        ))
        print("Avg Days of Use      %.2f                     %.2f             %.2f" % (
            in_days_of_use / in_total_users, out_days_of_use / out_total_users, bio180_days_of_use / bio180_total_users,)
        )
        print("1-1 Messages/User    %.2f                     %.2f             %.2f" % (
            in_one_to_one_messages / in_total_users,
            out_one_to_one_messages / out_total_users,
            bio180_one_to_one_messages / bio180_total_users,
        ))
