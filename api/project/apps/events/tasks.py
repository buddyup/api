import datetime
import json
import requests
import time
from binascii import hexlify
from simplecrypt import encrypt
from celery.task import task, periodic_task

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.template.loader import render_to_string
from django.utils import timezone

from events.handlers.base import AllEventHandlers, SYSTEM_CREATOR
from events.models import Event, PushTombstone, EmailTombstone,\
    GroupReminderTombstone, TimingTombstone, APITimingTombstone,\
    PushTimingTombstone
from gatekeeper.models import User

all_handlers = AllEventHandlers()

LAST_READ_OFFSET = 2000
INTERNATIONAL_CAMPUSES = ["sydney_edu_au", "unsw_edu_au"]


def now():
    return int(time.mktime(timezone.now().timetuple()) * 1000)


def firebase_url(endpoint, shallow=False):
    querystring = False
    if "?" in endpoint:
        querystring = endpoint.split("?")[1]
        endpoint = endpoint.split("?")[0]
    if not endpoint.endswith("/"):
        endpoint = "%s/" % endpoint
    if endpoint.startswith("/"):
        endpoint = endpoint[1:]

    if not querystring:
        url = "%s/%s.json?format=export&auth=%s" % (
            settings.FIREBASE_ENDPOINT,
            endpoint,
            settings.FIREBASE_KEY,
        )
    if querystring:
        url = "%s/%s.json?%s&format=export&auth=%s" % (
            settings.FIREBASE_ENDPOINT,
            endpoint,
            querystring,
            settings.FIREBASE_KEY,
        )

    if shallow:
        url = "%s&shallow=true" % url

    return url


@task
def firebase_put(endpoint, data, acks_late=True, shallow=False):
    # TODO: get endpoint make sure it hasn't been updated more recently.
    # print(firebase_url(endpoint))
    r = requests.put(firebase_url(endpoint, shallow=shallow), json.dumps(data))
    if not r.status_code == 200:
        print(r.status_code)
        print(r.json())
    assert r.status_code == 200


@task
def firebase_patch(endpoint, data, acks_late=True, shallow=False):
    # TODO: get endpoint make sure it hasn't been updated more recently.
    # print(firebase_url(endpoint, shallow=shallow))
    r = requests.patch(firebase_url(endpoint, shallow=shallow), json.dumps(data))
    if not r.status_code == 200:
        print(r.status_code)
        print(r.json())
    assert r.status_code == 200


@task
def firebase_post(endpoint, data, acks_late=True, shallow=False):
    r = requests.post(firebase_url(endpoint, shallow=shallow), json.dumps(data))
    if not r.status_code == 200:
        print(r.status_code)
        print(r.json())
    assert r.status_code == 200
    return r.json()


@task
def firebase_get(endpoint, acks_late=True, shallow=False):
    # r = requests.get(firebase_url(endpoint, shallow=shallow), json.dumps(data))
    r = requests.get(firebase_url(endpoint, shallow=shallow))
    if not r.status_code == 200:
        print(r.status_code)
        print(r.json())
    assert r.status_code == 200
    return r.json()


@task
def push_and_email(buid, push_type, event, push_type_values=["on", ], badge_count=1, acks_late=True):
    print("Push %s to %s" % (event["type"], buid))
    # TODO: handle target url

    # Handle Push
    private = firebase_get("/users/%s/private" % buid)
    # print("push_type_values")
    # print(push_type_values)
    # print(private)
    # print(event)

    # If they've read the screen more recently, skip it.

    skip = False
    if "last_reads" in private:
        if event["type"] == "buddy_request" and "buddy_requests" in private["last_reads"]:
            if private["last_reads"]["buddy_requests"] + LAST_READ_OFFSET >= event["created_at"]:
                skip = True
        elif event["type"] == "chat_message":
            if "group_id" in event["data"]:
                if (
                    event["data"]["group_id"] in private["last_reads"] and
                    private["last_reads"][event["data"]["group_id"]] + LAST_READ_OFFSET >= event["created_at"]
                ):
                    skip = True
            elif "class_id" in event["data"]:
                if (
                    event["data"]["class_id"] in private["last_reads"] and
                    private["last_reads"][event["data"]["class_id"]] + LAST_READ_OFFSET >= event["created_at"]
                ):
                    skip = True
        elif event["type"] == "created_group":
            if "subject" in event["data"]:
                if (
                    event["data"]["subject"] in private["last_reads"] and
                    private["last_reads"][event["data"]["subject"]] + LAST_READ_OFFSET >= event["created_at"]
                ):
                    skip = True

        # group_reminder and buddied_up
            # Always show.

        elif event["type"] == "private_message":
            if "sender" in event["data"]:
                last_read_key = 'thread-' + event["data"]["sender"]
                if (
                    last_read_key in private["last_reads"] and
                    private["last_reads"][last_read_key] + LAST_READ_OFFSET >= event["created_at"]
                ):
                    skip = True

    if skip:
        print("Skipping, since the user has looked more recently.")
        return

    u = User.objects.get(buid=buid)
    if push_type == "buddied_up":
        push_type = "buddy_request"
    context = {
        "event": event,
        "push_type": push_type,
        "django_user": u,
        "user": firebase_get("/users/%s/public" % buid)
    }
    if "data" in event and "class_id" in event["data"]:
        context["class"] = firebase_get("/classes/%s/profile" % event["data"]["class_id"])
    if "data" in event and "group_id" in event["data"]:
        context["group"] = firebase_get("/groups/%s/profile" % event["data"]["group_id"])

    # Changed, now that we have on/off
    if (
        "push_%s" % push_type in private and
        private["push_%s" % push_type] in ["everyone", "buddies", "on"]
    ):
        text = render_to_string("events/push/%s.txt" % event["type"], context)
        # print(text)
        push_data = {
            "production": True,
            "user_ids": [buid, ],
            "notification": {
                "alert": text,
                "ios": {
                    "badge": badge_count,
                    "sound": "ping.aiff",
                    "expiry": 1423238641,
                    "priority": 10,
                    "contentAvailable": True,
                    "payload": {
                        "key1": "value",
                        "key2": "value"
                    }
                },
                "android": {
                    "collapseKey": "foo",
                    "delayWhileIdle": True,
                    "timeToLive": 300,
                    "payload": {
                        "key1": "value",
                        "key2": "value"
                    }
                }
            }
        }

        push_headers = {
            'X-Ionic-Application-Id': settings.IONIC_APP_ID,
            'Content-Type': 'application/json',
        }

        r = requests.post(
            "https://push.ionic.io/api/v1/push",
            data=json.dumps(push_data),
            auth=(settings.IONIC_PRIVATE_KEY, ''),
            headers=push_headers
        )
        if not r.status_code < 300:
            print(r.status_code)
            print(r.json())
            # assert r.status_code < 300
        else:
            # print("pushed to %s" % u.email)
            # print(push_data)
            PushTombstone.objects.create(
                push_type=push_type,
                user_id=u.pk,
                buid=buid,
                event_id=event["event_id"],
                event=json.dumps(push_data),
            )

    # Handle email
    # print("email_%s" % push_type)
    if (
        "email_%s" % push_type in private and
        private["email_%s" % push_type] in ["everyone", "buddies", "on"]
    ):
        print("sending email to %s" % u.email)
        subject = render_to_string("events/email/%s.subject.txt" % event["type"], context)
        body = render_to_string("events/email/%s.body.txt" % event["type"], context)
        send_mail(subject, body, settings.SERVER_EMAIL, [u.email], fail_silently=False)

        EmailTombstone.objects.create(
            user_id=u.pk,
            buid=buid,
            event_id=event["event_id"],
            email=u.email,
            subject=subject,
            body=body,
        )


@task
def firebase_delete(endpoint, acks_late=True):
    r = requests.delete(firebase_url(endpoint))
    assert r.status_code == 200


@task(name="log_event", acks_late=True, time_limit=120)
def log_event(data):
    # Must be idempotent!!
    e, created = Event.objects.get_or_create(event_id=data["event_id"])
    if created or not e.event_timestamp or data["created_at"] > time.mktime(e.event_timestamp) * 1000:
        try:
            u = User.objects.get(buid=data["creator"])
            e.email = u.email
        except:
            print("User %s not found." % data["creator"])
        e.event_type = data["type"]
        e.creator = data["creator"]
        e.event_timestamp = datetime.datetime.fromtimestamp(int(data["created_at"]) / 1000)
        if "data" in data:
            e.data = hexlify(encrypt(settings.ACCESS_LOG_KEY, json.dumps(data["data"]).encode('utf8')))
        # print(e.__dict__)
        e.save()


@task(name="encrypt_event", acks_late=True, time_limit=240)
def encrypt_event(key, counter, total):
    e = Event.objects.get(pk=key)
    try:
        if e.data:
            decoded = json.loads(e.data)
            if decoded:
                e.data = hexlify(encrypt(settings.ACCESS_LOG_KEY, e.data.encode('utf8')))
                e.save()
    except:
        print("Error encrypting.")
        print(e.data)
        import traceback
        traceback.print_exc()
        print(" -- skipping, already encrypted")
        pass
    print("%s/%s events encrypted.  (%s)" % (counter, total, e.pk))


@task(name="handle_event", acks_late=True)
def handle_event(data):
    # Take the event, and place the results in all the correct bins (respecting blocks)

    # Log it
    log_event.delay(data)

    # Hand it off to the right handler.
    # Helper function that checks all classes, gets the right event_types matches.
    if data["type"] in all_handlers.handlers:
        for h in all_handlers.handlers[data["type"]]:
            handler = h(data)
            handler.handle()
    else:
        print("No event handlers found for '%s' event." % data["type"])
        # TODO: raise this to devs.

    print(data)


@periodic_task(run_every=datetime.timedelta(seconds=60))
def study_group_reminders():

    # Get the next 90 seconds of study groups, and send out reminders
    # TODO: Need to know how to limit queries via REST.
    # Could also tombstone here.
    # event.reminder_sent, then do startAt on it.

    url = "%s&orderBy=\"start\"&startAt=%s&endAt=%s" % (
        firebase_url("/groups/"),
        int(now() - (1000 * 60 * 200)),  # 2 minutes into the past (downtime, etc)
        int(now() + (1000 * 60 * 5)),  # 5 minutes into the future
    )

    r = requests.get(url)
    groups = r.json()
    assert r.status_code == 200

    reminder_type = "about_to_start"

    for group_id, group_data in groups.items():
        if GroupReminderTombstone.objects.filter(
            group_id=group_id,
            reminder_type=reminder_type
        ).count() == 0:
            send_group_reminder.delay(group_id, reminder_type)
            GroupReminderTombstone.objects.create(
                group_id=group_id,
                reminder_type=reminder_type,
            )
        else:
            # print("already sent")
            pass


@task
def send_group_reminder(group_id, reminder_type):
    n = now()
    data = {
        "creator": SYSTEM_CREATOR,
        "type": "group_reminder",
        "group_id": group_id,
        "reminder_type": reminder_type,
        "event_id": "group-reminder-%s-%s" % (group_id, now()),
        "created_at": n,
        "order": 10000000000000 - n,
    }
    handle_event(data)


@periodic_task(run_every=datetime.timedelta(seconds=15))
def start_timing():
    t = TimingTombstone.objects.create(
        started_at=timezone.now()
    )
    end_timing.delay(t.pk)


@task
def end_timing(timing_pk):
    end_now = timezone.now()
    t = TimingTombstone.objects.get(pk=timing_pk)
    t.finished_at = end_now
    t.save()
    t = TimingTombstone.objects.get(pk=timing_pk)
    t.difference = (t.finished_at - t.started_at).microseconds
    t.save()

    try:
        firebase_post("history/tasks/", {
            "t": now(),
            "v": t.difference / 1000
        })
        qs = TimingTombstone.objects.all().exclude(finished_at=None).order_by("-finished_at")[:5]
        qs = qs.aggregate(avg_time=Avg('difference'))
        if 'avg_time' in qs and qs['avg_time']:
            firebase_put("analytics/task_timing_last_5", {".value": qs['avg_time'] / 1000.0})

        qs = TimingTombstone.objects.all().exclude(finished_at=None).order_by("-finished_at")[:80]
        qs = qs.aggregate(avg_time=Avg('difference'))
        if 'avg_time' in qs and qs['avg_time']:
            firebase_put("analytics/task_timing_last_15_min", {".value": qs['avg_time'] / 1000.0})

        qs = TimingTombstone.objects.all().exclude(finished_at=None).order_by("-finished_at")[:240]
        qs = qs.aggregate(avg_time=Avg('difference'))
        if 'avg_time' in qs and qs['avg_time']:
            firebase_put("analytics/task_timing_last_hour", {".value": qs['avg_time'] / 1000.0})
    except:
        import traceback
        traceback.print_exc()
        pass


@periodic_task(run_every=datetime.timedelta(seconds=15))
def start_push_timing():
    t = PushTimingTombstone.objects.create(
        started_at=timezone.now()
    )
    end_push_timing.delay(t.pk)


@task
def end_push_timing(timing_pk):
    end_now = timezone.now()
    t = PushTimingTombstone.objects.get(pk=timing_pk)
    t.finished_at = end_now
    t.save()
    t = PushTimingTombstone.objects.get(pk=timing_pk)
    t.difference = (t.finished_at - t.started_at).microseconds
    t.save()

    try:
        firebase_post("history/push/", {
            "t": now(),
            "v": t.difference / 1000
        })
        qs = PushTimingTombstone.objects.all().exclude(finished_at=None).order_by("-finished_at")[:5]
        qs = qs.aggregate(avg_time=Avg('difference'))
        if 'avg_time' in qs and qs['avg_time']:
            firebase_put("analytics/push_timing_last_5", {".value": qs['avg_time'] / 1000.0})

        qs = PushTimingTombstone.objects.all().exclude(finished_at=None).order_by("-finished_at")[:80]
        qs = qs.aggregate(avg_time=Avg('difference'))
        if 'avg_time' in qs and qs['avg_time']:
            firebase_put("analytics/push_timing_last_15_min", {".value": qs['avg_time'] / 1000.0})

        qs = PushTimingTombstone.objects.all().exclude(finished_at=None).order_by("-finished_at")[:240]
        qs = qs.aggregate(avg_time=Avg('difference'))
        if 'avg_time' in qs and qs['avg_time']:
            firebase_put("analytics/push_timing_last_hour", {".value": qs['avg_time'] / 1000.0})
    except:
        import traceback
        traceback.print_exc()
        pass


@periodic_task(run_every=datetime.timedelta(minutes=30), time_limit=7200)
def sync_analytics():
    print("Syncing school data")
    total_num_students = 0
    total_study_groups = 0
    total_active_schools = 0
    total_seeder_schools = 0
    total_classes = 0
    total_seeders = 0

    schools = firebase_get("/schools")
    for name, data in schools.items():
        student_ids = []
        school_num_students = 0
        school_buddy_matches = 0
        school_study_groups = 0
        school_classes = 0
        num_students_in_groups = 0
        number_of_actions = 0

        if (
            "profile" in data and
            "active" in data["profile"] and
            data["profile"]["active"] is True
        ):
            total_active_schools += 1
        else:
            total_seeder_schools += 1

        if "students" in data:
            for id, student_data in data["students"].items():
                total_num_students += 1
                school_num_students += 1
                student_ids.append(id)

                if (
                    "profile" not in data or
                    "active" not in data["profile"] or
                    not data["profile"]["active"]
                ):
                    total_seeders += 1

        if "groups" in data:
            for id, group_data in data["groups"].items():
                total_study_groups += 1
                school_study_groups += 1
                attendees = firebase_get("groups/%s/attending" % id, shallow=True)
                if attendees:
                    num_students_in_groups += len(attendees.keys())
                news_feed = firebase_get("groups/%s/news_feed" % id, shallow=True)
                if news_feed:
                    number_of_actions += len(news_feed.keys())

        if "classes" in data:
            for id, class_data in data["classes"].items():
                total_classes += 1
                school_classes += 1
                news_feed = firebase_get("classes/%s/news_feed" % id, shallow=True)
                if news_feed:
                    number_of_actions += len(news_feed.keys())

        for user_id in student_ids:
            buddies = firebase_get("users/%s/buddies" % user_id, shallow=True)
            if buddies:
                school_buddy_matches += 1

                number_of_actions += len(buddies.keys())

        firebase_patch("/analytics/schools/%s/" % name, {
            "num_students": school_num_students,
            "buddy_matches": school_buddy_matches,
            "study_groups": school_study_groups,
            "classes": school_classes,
            "num_students_in_groups": num_students_in_groups,
            "number_of_actions": number_of_actions,
        })

    buddied_up_list = firebase_get("events?orderBy=\"type\"&startAt=\"buddied_up\"&endAt=\"buddied_up\"")
    num_buddied_up = len(buddied_up_list.keys())

    unbuddied_list = firebase_get("events?orderBy=\"type\"&startAt=\"unbuddied\"&endAt=\"unbuddied\"")
    num_unbuddied = len(unbuddied_list.keys())

    firebase_patch("/analytics", {
        "total_num_students": total_num_students,
        "total_buddy_matches": num_buddied_up - num_unbuddied,
        "total_study_groups": total_study_groups,
        "total_active_schools": total_active_schools,
        "total_seeder_schools": total_seeder_schools,
        "total_classes": total_classes,
        "total_seeders": total_seeders,
    })


def really():
    classes = firebase_get("/analytics/classes")
    presented_classes = []
    prof_email_classes = []
    # followup_email_classes = []
    piloted_classes = []
    for k, class_info in classes.items():
        if "presented" in class_info and class_info["presented"]:
            presented_classes.append(k)
            piloted_classes.append(k)
        if "prof_email" in class_info and class_info["prof_email"]:
            prof_email_classes.append(k)
            if k not in piloted_classes:
                piloted_classes.append(k)
        # if "followup_email" in class_info and class_info["followup_email"]:
        #     followup_email_classes.append(k)
        #     if k not in piloted_classes:
        #         piloted_classes.append(k)

    print(piloted_classes)
    num_in_piloted = 0
    num_viral = 0
    num_users = 0
    num_unknown = 0

    users = firebase_get("/users/", shallow=True)
    print("Checking %s users..." % len(users.keys()))
    for user_key, _ in users.items():
        print("User: %s" % user_key)
        user_classes = firebase_get("/users/%s/classes" % user_key, shallow=True)
        if user_classes:
            in_piloted_class = False
            for class_key, _ in user_classes.items():
                if class_key in piloted_classes:
                    in_piloted_class = True

            if in_piloted_class:
                num_in_piloted += 1
            else:
                num_viral += 1
        else:
            num_unknown += 1

        num_users += 1

    print("num_in_piloted")
    print(num_in_piloted)
    print("num_viral")
    print(num_viral)
    print("num_users")
    print(num_users)
    print("num_unknown")
    print(num_unknown)


@periodic_task(run_every=datetime.timedelta(minutes=5), time_limit=7200)
def sync_journey_analytics():

    signups_per_day_alpha = 0
    actions_per_user_alpha = 0
    viral_signups_per_day_alpha = 0
    average_user_opens_per_week_alpha = 0
    seeder_campuses_alpha = 0
    international_users_alpha = 0
    international_campuses_alpha = 0
    actions_per_user_per_day_alpha = 0

    signups_per_day_1_0 = 0
    actions_per_user_1_0 = 0
    viral_signups_per_day_1_0 = 0
    average_user_opens_per_week_1_0 = 0
    seeder_campuses_1_0 = 0
    international_users_1_0 = 0
    international_campuses_1_0 = 0
    actions_per_user_per_day_1_0 = 0

    signups_per_day_1_5 = 0
    actions_per_user_1_5 = 0
    viral_signups_per_day_1_5 = 0
    average_user_opens_per_week_1_5 = 0
    seeder_campuses_1_5 = 0
    international_users_1_5 = 0
    international_campuses_1_5 = 0
    actions_per_user_per_day_1_5 = 0

    # alpha
    today = datetime.datetime.now()
    year_start = datetime.datetime(year=2015, month=1, day=1)
    start_1_0 = datetime.datetime(year=2015, month=7, day=27)
    start_1_5 = datetime.datetime(year=2015, month=9, day=24)
    num_days_alpha = (start_1_0 - year_start).days
    days_1_0 = (start_1_5 - start_1_0).days
    days_1_5 = (today - start_1_5).days

    # Alpha data
    # Jan 1, 2015 - July 27, 2015

    # export.py, dropbox
    # total_viral_signups
    # 692
    # total_actions
    # 7636
    # num_users_who_opened_by_week
    # 1037

    # Intercom: Signed up in window, has bio=true
    signups_per_day_alpha = 465 / num_days_alpha
    #  /4 is to handle the page view counting.
    actions_per_user_alpha = 7636 / 465 / 4
    international_users_alpha = 0
    international_campuses_alpha = 0
    actions_per_user_per_day_alpha = actions_per_user_alpha / num_days_alpha

    # TODO
    seeder_campuses_alpha = 2
    viral_signups_per_day_alpha = 692 / num_days_alpha
    average_user_opens_per_week_alpha = 1206 / num_days_alpha / 7

    # Baseline data
    active_schools = []
    inactive_schools = []
    all_schools = firebase_get("/schools/", shallow=True)
    for k, t in all_schools.items():
        school_profile = firebase_get("/schools/%s/profile" % k,)
        if school_profile and ("active" in school_profile and school_profile["active"] is True):
            active_schools.append(k)
        else:
            inactive_schools.append(k)
    # signed_up", ]

    # def handle(self):
    #     school_id = self.cleaned_event["data"]["school_id"]

    # 1.0

    classes = firebase_get("/analytics/classes")
    presented_classes = []
    prof_email_classes = []
    # followup_email_classes = []
    piloted_classes = []
    for k, class_info in classes.items():
        if "presented" in class_info and class_info["presented"]:
            presented_classes.append(k)
            piloted_classes.append(k)
        if "prof_email" in class_info and class_info["prof_email"]:
            prof_email_classes.append(k)
            if k not in piloted_classes:
                piloted_classes.append(k)
        # if "followup_email" in class_info and class_info["followup_email"]:
        #     followup_email_classes.append(k)
        #     if k not in piloted_classes:
        #         piloted_classes.append(k)

    # print(piloted_classes)
    signups_1_0 = Event.objects.exclude(
        creator=SYSTEM_CREATOR
    ).filter(event_type="signed_up", created_at__lte=start_1_5).count()
    # opens_1_0 = Event.objects.exclude(
    #     creator=SYSTEM_CREATOR
    # ).filter(event_type="device_init", created_at__lte=start_1_5).count()
    actions_1_0 = Event.objects.exclude(creator=SYSTEM_CREATOR).filter(created_at__lte=start_1_5).count()
    num_users_1_0 = Event.objects.exclude(creator=SYSTEM_CREATOR).filter(created_at__lte=start_1_5).distinct("creator").count()

    viral_signups_1_0 = 0
    seeder_campuses_1_0_list = {}

    for u in User.objects.filter(created_at__lt=start_1_5):
        if u.main_school not in seeder_campuses_1_0_list and u.main_school not in active_schools:
            seeder_campuses_1_0_list[u.main_school] = True

    international_users_1_0 = 0
    international_campuses_1_0_list = {}
    viral_signup_users_1_0 = {}
    for s in Event.objects.exclude(creator=SYSTEM_CREATOR).filter(event_type="signed_up", created_at__lte=start_1_5).all():
        try:
            if s.data:
                data = json.loads(s.data)
                if data["school_id"] in INTERNATIONAL_CAMPUSES:
                    international_users_1_0 += 1
                    if data["school_id"] not in international_campuses_1_0_list:
                        international_campuses_1_0_list[data["school_id"]] = True

                class_adds = Event.objects.exclude(
                    creator=SYSTEM_CREATOR
                ).filter(event_type="added_class", creator=s.creator, created_at__lte=start_1_5)
                for c in class_adds:
                    in_piloted_class = False
                    if c.data:
                        class_id = json.loads(c.data)["id"]
                        if class_id in piloted_classes:
                            in_piloted_class = True
                            break
                    else:
                        print("No class data for %s" % c)

                    if not in_piloted_class and s.creator not in viral_signup_users_1_0:
                        viral_signups_1_0 += 1
                        viral_signup_users_1_0[s.creator] = True
        except:
            pass

    # for s in Event.objects.exclude(creator=SYSTEM_CREATOR).filter(event_type="signed_up", created_at__lte=start_1_5).all():

    signups_per_day_1_0 = signups_1_0 / (days_1_0 or 1)
    actions_per_user_1_0 = actions_1_0 / (num_users_1_0 or 1)
    viral_signups_per_day_1_0 = viral_signups_1_0 / (days_1_0 or 1)

    # average_user_opens_per_week_1_0 = opens_1_0 / (signups_1_0 or 1) / (days_1_0 or 1)
    seeder_campuses_1_0 = len(seeder_campuses_1_0_list.keys())
    international_campuses_1_0 = len(international_campuses_1_0_list.keys())
    actions_per_user_per_day_1_0 = actions_1_0 / (num_users_1_0 or 1) / (days_1_0 or 1)
    # start = start_1_0
    # weeks = 0
    num_opens = 0
    last_e = None
    events = Event.objects.exclude(creator=SYSTEM_CREATOR).filter(
        created_at__lte=start_1_5
    ).order_by("creator", "created_at").all()
    for e in events:
        if (
            not last_e or
            last_e.creator != e.creator or
            (e.created_at - last_e.created_at).total_seconds() >= 60
        ):
            num_opens += 1
            last_e = e

    average_user_opens_per_week_1_0 = num_opens / num_users_1_0 / (days_1_0 / 7)

    # num_opens = 0
    # while start <= start_1_5:
    #     one_week_out = start + datetime.timedelta(days=7)
    #     if one_week_out > start:
    #         one_week_out = start
    #     num_opens += Event.objects.exclude(creator=SYSTEM_CREATOR).filter(
    #         event_type="device_init",
    #         created_at__lte=one_week_out,
    #         created_at__gte=start
    #     ).distinct("creator").count()
    #     weeks + 1
    #     start += datetime.timedelta(days=7)
    # average_user_opens_per_week_1_0 = num_opens / (signups_1_0 or 1) / (weeks or 1)  # / 5 fudge for device_init bug

    # TODO: proper viral signups against marked classes.

    # 1.5

    signups_1_5 = Event.objects.exclude(
        creator=SYSTEM_CREATOR
    ).filter(event_type="signed_up", created_at__gt=start_1_5).count()
    # opens_1_5 = Event.objects.exclude(
    #     creator=SYSTEM_CREATOR
    # ).filter(event_type="device_init", created_at__lte=start_1_5).count()
    actions_1_5 = Event.objects.exclude(
        creator=SYSTEM_CREATOR
    ).filter(created_at__gt=start_1_5).count()
    num_users_1_5 = Event.objects.exclude(
        creator=SYSTEM_CREATOR
    ).filter(created_at__gt=start_1_5).distinct("creator").count()

    viral_signups_1_5 = 0

    # viral_signups_1_5_list = {}
    seeder_campuses_1_5_list = {}
    for u in User.objects.filter():
        if (
            u.main_school not in seeder_campuses_1_5_list and
            u.main_school not in active_schools
            # u.main_school not in seeder_campuses_1_0_list
        ):
            seeder_campuses_1_5_list[u.main_school] = True

    international_users_1_5 = 0
    international_campuses_1_5_list = {}
    viral_signup_users_1_5 = {}

    for s in Event.objects.exclude(creator=SYSTEM_CREATOR).filter(event_type="signed_up", created_at__gte=start_1_5).all():
        if s.data:
            data = json.loads(s.data)

            if data["school_id"] in INTERNATIONAL_CAMPUSES:
                international_users_1_5 += 1
                if data["school_id"] not in international_campuses_1_5_list:
                    international_campuses_1_5_list[data["school_id"]] = True

            # todo
            class_adds = Event.objects.exclude(
                creator=SYSTEM_CREATOR
            ).filter(event_type="added_class", creator=s.creator, created_at__gt=start_1_5)
            for c in class_adds:
                in_piloted_class = False
                if c.data:
                    data = json.loads(c.data)
                    class_id = data["id"]
                    if class_id in presented_classes:
                        in_piloted_class = True
                        break
                else:
                    print("No class data for %s" % c)

                if not in_piloted_class and s.creator not in viral_signup_users_1_5:
                    viral_signups_1_5 += 1
                    viral_signup_users_1_5[s.creator] = True

    signups_per_day_1_5 = signups_1_5 / (days_1_5 or 1)
    actions_per_user_1_5 = actions_1_5 / (signups_1_5 or 1)
    viral_signups_per_day_1_5 = viral_signups_1_5 / (days_1_5 or 1)

    # average_user_opens_per_week_1_5 = opens_1_5 / (signups_1_5 or 1) / (days_1_5 or 1)
    international_users_1_5 += international_users_1_0
    seeder_campuses_1_5 = len(seeder_campuses_1_5_list.keys())
    international_campuses_1_5 = len(international_campuses_1_5_list.keys())
    actions_per_user_per_day_1_5 = actions_1_5 / (signups_1_5 or 1) / (days_1_5 or 1)
    # start = start_1_5
    # weeks = 0
    # num_opens = 0
    # while start <= start_1_5:
    #     one_week_out = start + datetime.timedelta(days=7)
    #     if one_week_out > start:
    #         one_week_out = start
    #     num_opens += Event.objects.exclude(creator=SYSTEM_CREATOR).filter(
    #         event_type="device_init",
    #         created_at__gt=one_week_out,
    #         created_at__gte=start
    #     ).distinct("creator").count()
    #     weeks + 1
    #     start += datetime.timedelta(days=7)
    # average_user_opens_per_week_1_5 = num_opens / (signups_1_5 or 1) / (weeks or 1)  # / 5 fudge for device_init bug
    num_opens = 0
    last_e = None
    events = Event.objects.exclude(creator=SYSTEM_CREATOR).filter(
        created_at__gte=start_1_5
    ).order_by("creator", "created_at").all()
    for e in events:
        if (
            not last_e or
            last_e.creator != e.creator or
            (e.created_at - last_e.created_at).total_seconds() >= 60
        ):
            num_opens += 1
            last_e = e
    average_user_opens_per_week_1_5 = num_opens / num_users_1_5 / (days_1_5 / 7)

    international_campuses_1_0 = 2
    international_campuses_1_5 = 2

    data = {
        "num_days_alpha": num_days_alpha,
        "num_days_1_0": days_1_0,
        "num_days_1_5": days_1_5,
        "signups_per_day_alpha": signups_per_day_alpha,
        "actions_per_user_alpha": actions_per_user_alpha,
        "viral_signups_per_day_alpha": viral_signups_per_day_alpha,
        "average_user_opens_per_week_alpha": average_user_opens_per_week_alpha,
        "seeder_campuses_alpha": seeder_campuses_alpha,
        "international_users_alpha": international_users_alpha,
        "international_campuses_alpha": international_campuses_alpha,
        "actions_per_user_per_day_alpha": actions_per_user_per_day_alpha,
        "signups_per_day_1_0": signups_per_day_1_0,
        "actions_per_user_1_0": actions_per_user_1_0,
        "viral_signups_per_day_1_0": viral_signups_per_day_1_0,
        "average_user_opens_per_week_1_0": average_user_opens_per_week_1_0,
        "seeder_campuses_1_0": seeder_campuses_1_0,
        "international_users_1_0": international_users_1_0,
        "international_campuses_1_0": international_campuses_1_0,
        "actions_per_user_per_day_1_0": actions_per_user_per_day_1_0,
        "signups_per_day_1_5": signups_per_day_1_5,
        "actions_per_user_1_5": actions_per_user_1_5,
        "viral_signups_per_day_1_5": viral_signups_per_day_1_5,
        "average_user_opens_per_week_1_5": average_user_opens_per_week_1_5,
        "seeder_campuses_1_5": seeder_campuses_1_5,
        "international_users_1_5": international_users_1_5,
        "international_campuses_1_5": international_campuses_1_5,
        "actions_per_user_per_day_1_5": actions_per_user_per_day_1_5,
    }

    firebase_patch("/analytics/journey", data)


@periodic_task(run_every=datetime.timedelta(seconds=30))
def api_response():
    start = timezone.now()
    r = requests.get("%s/v1/speed" % settings.API_ENDPOINT)
    end = timezone.now()

    APITimingTombstone.objects.create(
        response_time=(end - start).microseconds,
        success=r.status_code == 200,
    )

    try:
        firebase_post("history/api/", {
            "t": now(),
            "v": (end - start).microseconds / 1000
        })
        qs = APITimingTombstone.objects.all().order_by("-created_at")[:5]
        qs = qs.aggregate(avg_time=Avg('response_time'))
        if 'avg_time' in qs and qs['avg_time']:
            firebase_put("analytics/api_response_last_5", {".value": qs['avg_time'] / 1000.0})

        qs = APITimingTombstone.objects.all().order_by("-created_at")[:40]
        qs = qs.aggregate(avg_time=Avg('response_time'))
        if 'avg_time' in qs and qs['avg_time']:
            firebase_put("analytics/api_response_last_15_min", {".value": qs['avg_time'] / 1000.0})

        qs = APITimingTombstone.objects.all().order_by("-created_at")[:120]
        qs = qs.aggregate(avg_time=Avg('response_time'))
        if 'avg_time' in qs and qs['avg_time']:
            firebase_put("analytics/api_response_last_hour", {".value": qs['avg_time'] / 1000.0})
    except:
        import traceback
        traceback.print_exc()
        pass


@periodic_task(run_every=datetime.timedelta(minutes=30))
def sync_all_class_analytics():
    print("Syncing class data")

    schools = firebase_get("/schools")
    for name, data in schools.items():
        # print(name)
        if (
            "profile" in data and
            "active" in data["profile"] and
            data["profile"]["active"] and
            "classes" in data
        ):

            for class_name in data["classes"].keys():
                sync_class_data.delay(class_name, data["profile"]["name"], name)

    firebase_put("analytics/last_classes_update", {".value": now()})


@task(time_limit=7200)
def sync_class_data(class_name, school_name, school_code):
    print("Sync class data: %s" % class_name)
    class_data = firebase_get("classes/%s/" % class_name)
    student_ids = []
    num_students = 0
    num_groups = 0
    num_with_one_buddy_in_class = 0
    num_buddies_in_class = 0
    num_buddies_at_school = 0
    num_students_in_groups = 0
    number_of_actions = 0

    if "students" in class_data:
        for id, student_data in class_data["students"].items():
            num_students += 1
            student_ids.append(id)

    is_pilot = False
    analytics = firebase_get("analytics/classes/%s/" % class_name)
    if analytics and (
        ("prof_email" in analytics and analytics["prof_email"] is True) or
        # ("followup_email" in analytics and analytics["followup_email"] is True) or
        ("presented" in analytics and analytics["presented"] is True)
    ):
        is_pilot = True

    if "groups" in class_data:
        for id, group_data in class_data["groups"].items():
            num_groups += 1

            attendees = firebase_get("groups/%s/attending" % id, shallow=True)
            if attendees:
                num_students_in_groups += len(attendees.keys())

            news_feed = firebase_get("groups/%s/news_feed" % id, shallow=True)
            if news_feed:
                number_of_actions += len(news_feed.keys())

    if "news_feed" in class_data:
        number_of_actions += len(class_data["news_feed"].keys())

    for user_id in student_ids:
        buddies = firebase_get("users/%s/buddies" % user_id, shallow=True)
        if buddies:
            has_in_class = False
            for id in buddies.keys():
                num_buddies_at_school += 1

                if id in student_ids:
                    num_buddies_in_class += 1
                    number_of_actions += 1
                    has_in_class = True

            if has_in_class:
                num_with_one_buddy_in_class += 1
    percent_buddied = 0
    if num_with_one_buddy_in_class and num_students:
        percent_buddied = 100.0 * num_with_one_buddy_in_class / num_students

    firebase_patch("/analytics/classes/%s/" % class_name, {
        "school": school_name,
        "school_code": school_code,
        "id": class_name,
        "name": class_data["profile"]["name"],
        "code": "%s %s" % (
            class_data["profile"]["subject_code"],
            class_data["profile"]["code"],
        ),
        "profile": class_data["profile"],
        "num_students": num_students,
        "num_groups": num_groups,
        "is_pilot": is_pilot,
        "number_of_actions": number_of_actions,
        "num_students_in_groups": num_students_in_groups,
        "num_with_one_buddy_in_class": num_with_one_buddy_in_class,
        "num_buddies_in_class": num_buddies_in_class,
        "num_buddies_at_school": num_buddies_at_school,
        "percent_buddied": percent_buddied,
    })


@periodic_task(run_every=datetime.timedelta(minutes=30))
def sync_app_ratings():
    print("Syncing app ratings")

    url = "https://api.appfigures.com/v2/ratings"
    headers = {
        'X-Client-Key': settings.APPFIGURES_CLIENT_KEY,
        'Content-Type': 'application/json',
    }
    data = {
        "start_date": "2015-06-01",
        "end_date": "2016-06-01",
        "countries": "US,AU",
        "group_by": "product",
    }
    r = requests.get(
        url,
        data=data,
        headers=headers,
        auth=(settings.APPFIGURES_USERNAME, settings.APPFIGURES_PASSWORD)
    )
    num = 0
    denom = 0
    last_review = None
    last_product = None
    for review in r.json():
        if last_product and last_product != review["product"]:
            last_product = review["product"]

            stars = last_review["stars"]
            print("adding %s" % stars)
            num += (stars[0] + 2 * stars[1] + 3 * stars[2] + 4 * stars[3] + 5 * stars[4])
            denom += sum(stars)

        last_product = review["product"]
        last_review = review

    stars = last_review["stars"]
    print("adding %s" % stars)
    num += (stars[0] + 2 * stars[1] + 3 * stars[2] + 4 * stars[3] + 5 * stars[4])
    denom += sum(stars)
    average = num / denom
    print(average)

    firebase_put("analytics/app/average_rating", {".value": round(average, 1)})
