import json
import requests
from binascii import hexlify
from simplecrypt import encrypt

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from celery.task import task
from utils.email import get_school_key_from_email

from gatekeeper.models import LoginAttempt, PasswordChangeAttempt,\
    SignupAttempt, User, DeleteAttempt, AccountCheckAttempt


@task(name="log_signup_attempt", acks_late=True)
def log_signup_attempt(data, ip, successful):
    SignupAttempt.objects.create(
        # attempt_full_name=data["full_name"],
        attempt_email=data["email"],
        attempt_password=hexlify(encrypt(settings.ACCESS_LOG_KEY, data["password"].encode('utf8'))),
        # attempt_terms=data["agreed_to_terms"],
        attempting_ip=ip,
        successful=successful
    )


@task(name="log_delete_attempt", acks_late=True)
def log_delete_attempt(data, ip, successful):
    DeleteAttempt.objects.create(
        # attempt_full_name=data["full_name"],
        # attempt_email=data["email"],
        attempt_password=hexlify(encrypt(settings.ACCESS_LOG_KEY, data["password"].encode('utf8'))),
        # attempt_terms=data["agreed_to_terms"],
        attempting_ip=ip,
        successful=successful
    )


@task(name="log_access_attempt", acks_late=True)
def log_access_attempt(email, password, ip, successful):
    LoginAttempt.objects.create(
        attempt_email=email,
        attempt_password=hexlify(encrypt(settings.ACCESS_LOG_KEY, password.encode('utf8'))),
        attempting_ip=ip,
        successful=successful
    )


@task(name="log_account_check_attempt", acks_late=True)
def log_account_check_attempt(email, ip, successful):
    AccountCheckAttempt.objects.create(
        attempt_email=email,
        attempting_ip=ip,
        successful=successful
    )


@task(name="log_password_attempt", acks_late=True)
def log_password_attempt(buid, ip, successful):
    PasswordChangeAttempt.objects.create(
        attempt_buid=buid,
        attempting_ip=ip,
        successful=successful
    )


def notify_will(url, data):
    print(data)
    if "email" in data:
        from utils.school_data import school_data

        school_key = get_school_key_from_email(data["email"])
        data["school"] = school_data[school_key]

    try:
        url = "%s/api%s" % (settings.WILL_URL, url)
        print(url)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(
            url,
            headers=headers,
            data=json.dumps(data),
        )
        if not r.status_code == 200:
            print(r.status_code)
            print(r.json())
    except:
        import traceback
        traceback.print_exc()


@task(name="new_signup", acks_late=True)
def notify_new_signup(buid, school_name):
    u = User.objects.get(pk=buid)
    data = {
        "email": u.email,
        "school_name": school_name,
    }

    notify_will("/signup", data)


@task(name="new_group", acks_late=True)
def notify_new_group(buid, event):
    u = User.objects.get(buid=buid)
    data = {
        "email": u.email,
        "event": event,
    }

    notify_will("/group", data)


@task(name="new_class", acks_late=True)
def notify_new_class(user_id, event):
    u = User.objects.get(buid=user_id)
    data = {
        "email": u.email,
        "event": event,
    }

    notify_will("/class", data)


@task(name="send_verification_email", acks_late=True)
def send_verification_email(user_id):
    print("send_verification_email")
    u = User.objects.get(pk=user_id)

    context = {
        "user": u,
    }
    subject = render_to_string('gatekeeper/confirm_email.subject.txt', context).replace("\n", "")
    body = render_to_string('gatekeeper/confirm_email.body.txt', context)

    send_mail(subject, body, settings.SERVER_EMAIL, [u.email], fail_silently=False)
    print("sent")


@task(name="delete_user", acks_late=True, time_limit=7200)
def delete_user(user_pk):
    from events.tasks import firebase_url, firebase_put, firebase_patch, firebase_post, firebase_get, firebase_delete
    u = User.objects.get(pk=user_pk)
    print("deleting %s" % u.buid)

    profile = firebase_get("/users/%s/public" % u.buid)
    profile["email"] = u.email
    # Remove from classes
    print("""users/%s/classes""")
    resp = firebase_get("/users/%s/classes" % u.buid)
    if resp:
        for class_id, info in resp.items():
            # Students list
            firebase_delete("/classes/%s/students/%s" % (class_id, u.buid))

            # News feed
            feed = firebase_get("/classes/%s/news_feed/" % class_id)
            if feed:
                for feed_id, item in feed.items():
                    if item["creator"] == u.buid:
                        firebase_delete("/classes/%s/news_feed/%s" % (class_id, feed_id))

    # Remove from buddies
    print("""users/%s/buddies/""")
    resp = firebase_get("/users/%s/buddies/" % u.buid)
    if resp:
        for buddy_id, item in resp.items():
            firebase_delete("/users/%s/buddies/%s" % (buddy_id, u.buid))

    # Pending requests incoming
    print("""users/%s/buddy_requests/""")
    resp = firebase_get("/users/%s/buddy_requests/" % u.buid)
    if resp:
        for buddy_id, item in resp.items():
            firebase_delete("/users/%s/buddies-outgoing/%s" % (buddy_id, u.buid))

    # Pending requests outgoing
    print("""users/%s/buddies-outgoing/""")
    resp = firebase_get("/users/%s/buddies-outgoing/" % u.buid)
    if resp:
        for buddy_id, item in resp.items():
            firebase_delete("/users/%s/buddy_requests/%s" % (buddy_id, u.buid))

    # Blocked
    # Skipping for now.. ?

    # Remove from inboxes
    print("""users/%s/inbox/""")
    resp = firebase_get("/users/%s/inbox/" % u.buid)
    if resp:
        for buddy_id, item in resp.items():
            # Remove threads from both people.
            thread_id = item["thread_id"]

            firebase_delete("/users/%s/inbox/%s" % (buddy_id, u.buid))
            firebase_delete("/message_threads/%s/" % (thread_id))

    # Remove from groups
    print("""users/%s/groups""")
    resp = firebase_get("/users/%s/groups" % u.buid)
    if resp:
        for group_id, item in resp.items():

            # Attending list
            firebase_delete("/groups/%s/attending/%s" % (group_id, u.buid))

            # If created the group... ?
            if item["creator"] == u.buid:
                # Remove all attendees
                print("""groups/%""")
                resp = firebase_get("/groups/%s/attending/" % group_id)
                if resp:
                    for attendee_id, item in resp.items():
                        firebase_delete("/user/%s/groups/%s" % (attendee_id, group_id))

                    # Delete it from class
                    if item["profile"] and item["profile"]["subject"]:
                        firebase_delete("/classes/%s/groups/%s" % (
                            item["profile"]["subject"],
                            group_id
                        ))

                    # Delete it from school
                    if item["school_id"]:
                        firebase_delete("/schools/%s/groups/%s" % (
                            item["school_id"],
                            group_id
                        ))

                # Delete it.
                firebase_delete("/groups/%s" % group_id)

    # Remove from main event feed
    print("events")
    event_list = firebase_get(
        "events?orderBy=\"creator\"&startAt=\"%s\"&endAt=\"%s\"" % (u.buid, u.buid)
    )
    if event_list:
        for event_id, item in event_list.items():
            print(event_id)
            firebase_delete("/events/%s" % event_id)

    # print("""users/%s/news_feed""")
    # resp = firebase_get("/users/%s/news_feed" % u.buid)
    # if resp:
    #     for id, action in resp.items():
    #         # Do we remove from main firebase event list?
    #         print(id)
    #         print(action["type"])

    # All types of events: covered.
    # if action["type"] == "resend_verification_email":
    #     pass
    # elif action["type"] == "unbuddied":
    #     pass
    # elif action["type"] == "ignored_request":
    #     pass
    # elif action["type"] == "buddy_request":
    #     pass
    # elif action["type"] == "cancel_buddy_request":
    #     pass
    # elif action["type"] == "blocked":
    #     pass
    # elif action["type"] == "unblocked":
    #     pass
    # elif action["type"] == "report_content":
    #     pass
    # elif action["type"] == "cancel_report_content":
    #     pass
    # elif action["type"] == "thread_created":
    #     pass
    # elif action["type"] == "private_message":
    #     pass
    # elif action["type"] == "added_class":
    #     pass
    # elif action["type"] == "dropped_class":
    #     pass
    # elif action["type"] == "updated_group":
    #     pass
    # elif action["type"] == "attending_group":
    #     pass
    # elif action["type"] == "cancel_group_attend":
    #     pass
    # elif action["type"] == "group_reminder":
    #     pass
    # elif action["type"] == "account_created":
    #     pass
    # elif action["type"] == "signed_up":
    #     pass
    # elif action["type"] == "logged_in":
    #     pass
    # elif action["type"] == "update_profile_pic":
    #     pass
    # elif action["type"] == "delete_account":
    #     pass

    # Do the final wipe.

    # Remove from schools
    print("""users/%s/schools""")
    resp = firebase_get("/users/%s/schools" % u.buid)
    if resp:
        for school_id, item in resp.items():

            # Students list
            firebase_delete("/schools/%s/students/%s" % (school_id, u.buid))

    firebase_put("/users/%s/" % u.buid, {"deleted": {"marked_for_delete": True}})
    u.delete()

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(
        "%s/api/account-deleted" % settings.WILL_URL,
        headers=headers,
        data=json.dumps(profile)
    )
    assert r.status_code == 200


@task(name="merge_classes", acks_late=True, time_limit=7200)
def merge_classes(master_id=None, child_id=None):
    from events.tasks import firebase_url, firebase_put, firebase_patch,\
        firebase_post, firebase_get, firebase_delete, sync_class_data
    assert master_id and child_id
    print("Merging %s into %s" % (child_id, master_id))

    master_profile = firebase_get("/classes/%s/profile/" % (master_id,))
    child_profile = firebase_get("/classes/%s/profile/" % (child_id,))
    # - add class for each student
    child_students = firebase_get("/classes/%s/students/" % (child_id,))

    if child_students:

        master_data = {
            "id": master_id,
            "course_id": master_id,
            "name": master_profile["name"],
            "code": master_profile["code"],
            "school_id": master_profile["school_id"],
            "subject_code": master_profile["subject_code"],
            "subject_name": master_profile["subject_name"],
            "subject_icon": master_profile["subject_icon"],
        }
        for student, student_data in child_students.items():
            firebase_put("/users/%s/classes/%s/" % (student, master_id), master_data)
            # add to master class list
            firebase_put("/classes/%s/students/%s/" % (master_id, student), {".value": True})

        # - remove old class from students
        for student, student_data in child_students.items():
            firebase_delete("/users/%s/classes/%s/" % (student, child_id))

    # - update any study groups to new class
    groups = firebase_get("/classes/%s/groups/" % (child_id,))
    if groups:
        for group_id, group_data in groups.items():
            group_data["subject"] = master_id
            firebase_put("/classes/%s/groups/%s" % (master_id, group_id,), group_data)

    # remove class from school.
    firebase_delete("/schools/%s/classes/%s/" % (child_profile["school_id"], child_id))

    # pull from analytics
    firebase_delete("/analytics/classes/%s/" % child_id)

    # Update master analytics
    school_profile = firebase_get("/schools/%s/profile" % master_profile["school_id"])
    sync_class_data.delay(master_id, school_profile["name"], master_profile["school_id"])

    # - add message to chat?

    # - delete old class
    firebase_delete("/classes/%s/" % child_id)
    print("Merge complete.")
