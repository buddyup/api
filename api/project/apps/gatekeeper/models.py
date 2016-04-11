import datetime
import hashlib
import random
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.template.loader import render_to_string


from utils.models import BaseModel
from utils.email import get_school_key_from_email
from firebase_token_generator import create_token


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        u = self.create(email=email)
        u.set_password(password)
        u.save()

    def create_superuser(self, email, password):
        return self.create_user(email, password)


class User(AbstractBaseUser, BaseModel):
    email = models.CharField(max_length=254, unique=True, db_index=True)
    email_verified = models.BooleanField(default=False)
    email_confirm_key = models.CharField(blank=True, null=True, max_length=512, unique=True, db_index=True)
    main_school = models.CharField(blank=True, null=True, max_length=512, db_index=True)
    staff_flag = models.BooleanField(default=False)
    agreed_to_terms = models.BooleanField(default=False)
    must_reset_password = models.BooleanField(default=False)
    fire_jwt_cached = models.CharField(blank=True, null=True, max_length=512, unique=True)
    api_jwt_cached = models.CharField(blank=True, null=True, max_length=512, unique=True)
    buid = models.CharField(blank=True, null=True, max_length=512, unique=True, db_index=True)
    reset_key = models.CharField(blank=True, null=True, max_length=512, unique=True, db_index=True)

    # profile pics on S3
    pic_original = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    pic_medium = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    pic_tiny = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    # migrated data
    migrated_user = models.BooleanField(default=False)
    migrated_first_name = models.CharField(blank=True, null=True, max_length=254)
    migrated_last_name = models.CharField(blank=True, null=True, max_length=254)
    migrated_school = models.CharField(blank=True, null=True, max_length=254)
    has_signed_in = models.BooleanField(default=False)
    migration_password = models.CharField(blank=True, null=True, max_length=254)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __unicode__(self):
        return "%s" % (self.email,)

    def save(self, *args, **kwargs):
        if not self.email_confirm_key:
            salt = hashlib.sha1(str(random.random()).encode("utf-8")).hexdigest()[:5]
            self.email_confirm_key = hashlib.sha1(
                salt.encode("utf-8") + self.email.encode("utf-8")
            ).hexdigest()

        if not self.main_school and self.email:
            self.main_school = get_school_key_from_email(self.email)
        # TODO: if we allow people to change their emails, add a hook to sync it to firebase.
        super(User, self).save(*args, **kwargs)

    @property
    def info(self):
        return {
            "email": self.email,
            "must_reset_password": self.must_reset_password,
            "api_jwt": self.api_jwt,
            "fire_jwt": self.fire_jwt,
            "buid": self.buid,
        }

    @property
    def api_jwt(self):
        if not self.api_jwt_cached:
            h = hashlib.new('SHA512')
            h.update(str("USER_HASH_%s" % self.buid).encode('utf-8'))
            self.api_jwt_cached = h.hexdigest()
            self.save()
        return self.api_jwt_cached

    @property
    def is_staff(self):
        return (
            self.email.endswith("buddyup.org") and
            self.staff_flag is True and
            self.email_verified is True
        )

    @property
    def fire_jwt(self):
        # TODO: Decide on this.
        if True or not self.fire_jwt_cached:
            auth_payload = {"uid": self.buid, "buid": self.buid, "is_staff": self.is_staff}
            token = create_token(settings.FIREBASE_KEY, auth_payload)
            self.fire_jwt_cached = token
            self.save()
        return self.fire_jwt_cached

    def verify_fire_jwt(self):
        pass

    @property
    def total_events(self):
        from events.tasks import firebase_get
        data = firebase_get("/users/%s/events" % self.buid, shallow=True)
        if data:
            return len(data.keys())
        else:
            return 0

    @property
    def total_classes(self):
        from events.tasks import firebase_get
        data = firebase_get("/users/%s/classes" % self.buid, shallow=True)
        if data:
            return len(data.keys())
        else:
            return 0

    @property
    def scaffold_data(self):
        return {
            "private": {
                # "push_hearts": 'everyone',
                "push_groups": 'everyone',
                "push_classes": 'everyone',
                "push_buddy_request": 'on',
                "push_private_message": 'on',
                "push_my_groups": 'on',
                # "email_hearts": 'buddies',
                "email_classes": 'buddies',
                "email_groups": 'everyone',
                "email_buddy_request": 'on',
                "email_private_message": 'on',
                "email_my_groups": 'on',
                # "placeholder": True,
                # "notification_preferences": {"placeholder": True},
                # "buddy_search": {"placeholder": True},
                "migrated_user": self.migrated_user,
                "email": self.email,
            },
            "public": {},
            "buddies": {},
            "buddy_requests": {},
            # "events": {"placeholder": True},
            # "my_hearts": {"placeholder": True},
            # "buddies_hearts": {"placeholder": True},
            # "classes": {},
            # "groups": {"placeholder": True},
            # "schools": {"placeholder": True},
            # "inbox": {"placeholder": True},
            # "news_feed": {"placeholder": True},
            # "public": {"placeholder": True},
        }

    def send_reset_key(self):
        now = datetime.datetime.now()
        rand_int = random.randint(0, 999999999)
        h = hashlib.new('SHA1')
        h.update(str("RESET_KEY_%s_%s" % (now, rand_int)).encode('utf-8'))
        self.reset_key = h.hexdigest()
        self.save()
        context = {
            "user": self,

        }

        subject = render_to_string("gatekeeper/reset.subject.txt", context)
        body = render_to_string("gatekeeper/reset.body.txt", context)
        send_mail(subject, body, settings.SERVER_EMAIL, [self.email], fail_silently=False)


class LoginAttempt(BaseModel):
    successful = models.BooleanField(default=False)
    attempt_email = models.TextField(blank=True, null=True)
    attempt_password = models.TextField(blank=True, null=True)
    attempting_ip = models.CharField(max_length=255, blank=True, null=True)

    @property
    def attempt_time(self):
        return self.created_at


class AccountCheckAttempt(BaseModel):
    successful = models.BooleanField(default=False)
    attempt_email = models.TextField(blank=True, null=True)
    attempting_ip = models.CharField(max_length=255, blank=True, null=True)

    @property
    def attempt_time(self):
        return self.created_at


class PasswordChangeAttempt(BaseModel):
    successful = models.BooleanField(default=False)
    attempt_buid = models.TextField(blank=True, null=True)
    attempting_ip = models.CharField(max_length=255, blank=True, null=True)

    @property
    def attempt_time(self):
        return self.created_at


class SignupAttempt(BaseModel):
    attempt_full_name = models.TextField(blank=True, null=True)
    attempt_email = models.TextField(blank=True, null=True)
    attempt_password = models.TextField(blank=True, null=True)
    attempt_terms = models.BooleanField(default=False)
    attempting_ip = models.CharField(max_length=255, blank=True, null=True)
    successful = models.BooleanField(default=False)

    @property
    def attempt_time(self):
        return self.created_at


class DeleteAttempt(BaseModel):
    attempt_full_name = models.TextField(blank=True, null=True)
    attempt_email = models.TextField(blank=True, null=True)
    attempt_password = models.TextField(blank=True, null=True)
    attempt_terms = models.BooleanField(default=False)
    attempting_ip = models.CharField(max_length=255, blank=True, null=True)
    successful = models.BooleanField(default=False)

    @property
    def attempt_time(self):
        return self.created_at
