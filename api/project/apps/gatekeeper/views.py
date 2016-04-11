import datetime
import json
import time

from django.conf import settings
from django.core.mail import mail_admins
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from annoying.decorators import render_to, ajax_request

from gatekeeper.models import User
from gatekeeper.tasks import (
    log_access_attempt, log_password_attempt,
    log_signup_attempt, notify_new_signup, log_account_check_attempt,
    send_verification_email, log_delete_attempt, delete_user, merge_classes
)
from events.tasks import firebase_put, firebase_post
from events.handlers.events.profile import UpdateProfilePicHandler
from utils.school_data import school_data
from utils.email import get_school_key_from_email
from utils.factory import Factory

CORRECT_PASSWORD_STRING = "!!CORRECT!!BuddyUp"


@render_to("gatekeeper/home.html")
def home(request):
    return locals()


@render_to("gatekeeper/email_confirmation.html")
def confirm_email(request, email_key):
    u = User.objects.get(email_confirm_key=email_key)
    u.email_verified = True
    u.save()
    email_confirmed = True
    firebase_put("users/%s/internal/email_verified" % u.buid, {".value": True})
    return locals()


@ajax_request
@csrf_exempt
def user_authenticate(request):

    resp = {
        "success": False,
    }
    data = None
    if request.body:
        data = json.loads(request.body.decode('utf-8'))
    if data and "email" in data and "password" in data:
        data["email"] = data["email"].lower()
        user = authenticate(username=data["email"], password=data["password"])
        if user is not None and user.is_active and (
            "gc" not in data or data["gc"] is False or user.is_staff
        ):
            login(request, user)
            resp = user.info
            resp["success"] = True

    if resp["success"]:
        password = CORRECT_PASSWORD_STRING
    else:
        password = data["password"]
    log_access_attempt.delay(
        data["email"],
        password,
        request.META["REMOTE_ADDR"],
        resp["success"],
    )

    return resp


@ajax_request
@csrf_exempt
def user_signup(request):

    resp = {}
    error_message = ""
    success = False
    data = None
    if request.body:
        data = json.loads(request.body.decode('utf-8'))

    data["email"] = data["email"].lower()
    school_key = get_school_key_from_email(data["email"])
    if not data:
        error_message = "Error in submission. Please try again."
    elif"email" not in data:
        error_message = "Missing email"
    elif not school_key or school_key not in school_data:
        error_message = "Email must be a valid educational address."
        print(school_key)
    elif "password" not in data:
        error_message = "Missing password"
    # elif "full_name" not in data:
    #     error_message = "Missing your full name"
    # elif "agreed_to_terms" not in data or data["agreed_to_terms"] is not True:
    #     error_message = "You must agree to the terms"
    elif User.objects.filter(email=data["email"]).count() > 0:
        return user_authenticate(request)
        # error_message = "An account with this email exists. Try signing in?"
    else:

        u = User.objects.create(
            email=data["email"],
            agreed_to_terms=True
        )
        u.set_password(data["password"])
        u.save()

        user = authenticate(username=data["email"], password=data["password"])
        if user is not None and user.is_active:

            login(request, user)
            structure = user.scaffold_data
            structure["schools"] = {
                "%s" % (school_key,): {
                    "id": school_key,
                    "name": school_data[school_key]["name"],
                }
            }
            now = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
            structure["public"]["signed_up_at"] = now
            structure["public"]["buid"] = user.buid

            # Ensure basic firebase structure.
            resp_json = firebase_post("/users/", structure)
            user.buid = resp_json["name"]
            user.save()

            # Put the buid on the profile properly.
            structure["public"]["buid"] = user.buid
            firebase_put("/users/%s/public/buid" % user.buid, {
                ".value": user.buid
            })

            url = "/schools/%(school_id)s/students/%(creator)s/" % {
                "school_id": school_key,
                "creator": user.buid,
            }
            firebase_post(url, True)

            resp = user.info
            success = True

            notify_new_signup.delay(user.pk, school_data[school_key]["name"])
            send_verification_email.delay(user.pk)

        log_access_attempt.delay(
            data["email"],
            CORRECT_PASSWORD_STRING,
            request.META["REMOTE_ADDR"],
            success,
        )

        # Put in firebase.
        # names = data["full_name"].split(" ")
        # first_name = names[0]
        # last_name = ""
        # if len(names) > 1:
        #     last_name = "".join(names[1:])

    if success:
        data["password"] = CORRECT_PASSWORD_STRING

    log_signup_attempt.delay(
        data,
        request.META["REMOTE_ADDR"],
        success,
    )

    resp["success"] = success
    resp["error_message"] = error_message

    return resp


@ajax_request
@csrf_exempt
def confirm_delete(request):

    resp = {}
    error_message = ""
    success = False
    data = None
    if request.body:
        data = json.loads(request.body.decode('utf-8'))

    if not data:
        error_message = "Error in submission. Please try again."
    try:

        if data and "buid" in data and "api_jwt" in data and "password" in data and "confirmed" in data:
            user = User.objects.get(buid=data["buid"])
            assert user.api_jwt == data["api_jwt"]
            assert data["confirmed"] is True
            # check password.
            if user.check_password(data["password"]):
                success = True
                delete_user.delay(user.pk)
            else:
                error_message = "Password does not match."
        else:
            error_message = "Wrong credentials. This attempt was logged."

    except:
        error_message = "Wrong credentials. This attempt was logged."

    if error_message != "":
        mail_admins("Attempt to delete with invalid credentials", """
%s

%s

%s
        """ % (error_message, data, request))

    log_delete_attempt.delay(
        data,
        request.META["REMOTE_ADDR"],
        success,
    )

    resp["success"] = success
    resp["error_message"] = error_message

    return resp


@ajax_request
@csrf_exempt
def migrate_user(request):

    resp = {}
    error_message = ""
    success = False
    data = None
    if request.body:
        data = json.loads(request.body.decode('utf-8'))

    assert data["secret"] == settings.FIREBASE_KEY

    data["email"] = data["email"].lower()
    school_key = get_school_key_from_email(data["email"])
    print(school_key)
    if school_key != data["school_code"]:
        error_message = "Email and school code don't match."
    elif not data:
        error_message = "Error in submission. Please try again."
    elif "email" not in data:
        error_message = "Missing email"
    elif not school_key or school_key not in school_data:
        error_message = "Email must be a valid educational address."
    else:

        if User.objects.filter(email=data["email"]).count() == 0:
            temp_password = Factory.temp_password()
            user = User.objects.create(
                email=data["email"],
                created_at=data["created_at"],
                email_verified=True,
                agreed_to_terms=True,
                migrated_user=True,
                migration_password=temp_password,
                migrated_school=data["school_code"],
                migrated_first_name=data["first_name"],
                migrated_last_name=data["last_name"],
                must_reset_password=True
            )
            user.set_password(temp_password)
            user.save()
            created = True
        else:
            success = True
            created = False
            user = User.objects.filter(email=data["email"])[0]
            user.migrated_school = data["school_code"]
            user.migrated_first_name = data["first_name"]
            user.migrated_last_name = data["last_name"]
            user.must_reset_password = True
            user.email_verified = True
            user.migrated_user = True
            user.save()

            print("%s already added." % data["email"])

        if created or not user.buid:
            structure = user.scaffold_data
            structure["schools"] = {
                "%s" % (school_key,): {
                    "id": school_key,
                    "name": school_data[school_key]["name"],
                }
            }
            structure["public"]["signed_up_at"] = data["created_at"]

            # Ensure basic firebase structure.
            resp_json = firebase_post("/users/", structure)
            user.buid = resp_json["name"]
            user.save()

            firebase_put("/users/%s/public/buid" % user.buid, {
                ".value": user.buid
            })

            url = "/schools/%(school_id)s/students/%(creator)s/" % {
                "school_id": school_key,
                "creator": user.buid,
            }
            firebase_post(url, True)

            resp = user.info
            success = True
            print("Saved %s" % user)
            print(user.pk)

            # notify_new_signup.delay(user.pk, school_data[school_key]["name"])
            # send_verification_email.delay(user.pk)
        resp["buid"] = user.buid
        resp["created_at"] = int(time.mktime(user.created_at.timetuple()) * 1000)

    resp["success"] = success
    if error_message != "":
        print(error_message)
    resp["error_message"] = error_message
    return resp


@ajax_request
@csrf_exempt
def migrate_picture(request):
    resp = {}
    data = None
    if request.body:
        data = json.loads(request.body.decode('utf-8'))

    assert data["secret"] == settings.FIREBASE_KEY
    # print(data)
    buid = data["buid"]
    # print(buid)
    user = User.objects.get(buid=data["buid"])

    event = {
        "type": "update_profile_pic",
        "creator": buid,
    }
    handler = UpdateProfilePicHandler(event)
    handler.handle()

    resp["success"] = True
    resp["buid"] = user.buid
    return resp


@ajax_request
@csrf_exempt
def change_password(request):

    resp = {
        "success": False,
    }
    data = None
    if request.body:
        data = json.loads(request.body.decode('utf-8'))

    if data and "buid" in data and "api_jwt" in data and "password" in data:
        user = User.objects.get(buid=data["buid"])
        assert user.api_jwt == data["api_jwt"]
        user.set_password(data["password"])
        user.must_reset_password = False

        if user.migrated_user:
            user.has_signed_in = True

        user.save()
        resp["success"] = True

    log_password_attempt.delay(
        data["buid"],
        request.META["REMOTE_ADDR"],
        resp["success"],
    )

    return resp


@ajax_request
@csrf_exempt
def reset_password(request):

    resp = {
        "success": False,
        "error": "",
    }
    data = None
    if request.body:
        data = json.loads(request.body.decode('utf-8'))

    try:
        if data and "email" in data:
            if User.objects.filter(email=data["email"]).count() != 1:
                resp["error"] = "No account with that email."
            else:
                user = User.objects.get(email=data["email"])
                user.send_reset_key()
                resp["success"] = True

        log_password_attempt.delay(
            data["buid"],
            request.META["REMOTE_ADDR"],
            resp["success"],
        )
    except:
        import traceback
        traceback.print_exc()
        pass

    return resp


@render_to("gatekeeper/password_reset_confirmation.html")
def confirm_reset(request, email_key):
    saved = False
    try:
        u = User.objects.get(reset_key=email_key)

        if request.method == "POST":
            if request.POST["new_password"]:
                u.set_password(request.POST["new_password"])
                u.save()
                saved = True

        else:
            pass
    except:
        pass
    return locals()


@ajax_request
@csrf_exempt
def check_new_account(request):

    resp = {
        "success": False,
        "newAccount": True,
    }
    data = None
    if request.body:
        data = json.loads(request.body.decode('utf-8'))

    try:
        if data and "email" in data:
            resp["success"] = True

            User.objects.get(email=data["email"])
            resp["newAccount"] = False

            log_account_check_attempt.delay(
                data["email"],
                request.META["REMOTE_ADDR"],
                resp["success"],
            )
    except:
        import traceback
        traceback.print_exc()
        pass

    return resp


@ajax_request
@csrf_exempt
def handle_merge_class_request(request):

    resp = {
        "success": False,
        "merged": True,
    }
    data = None
    if request.body:
        data = json.loads(request.body.decode('utf-8'))

    try:
        if data and "buid" in data and "api_jwt" in data and "master" in data and "child" in data:
            user = User.objects.get(buid=data["buid"])
            assert user.api_jwt == data["api_jwt"]
            assert user.is_staff

            print(data)
            merge_classes.delay(master_id=data["master"], child_id=data["child"])
            resp["success"] = True

    except:
        import traceback
        traceback.print_exc()
        pass

    return resp
