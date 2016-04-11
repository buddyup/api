from django.db import models

from utils.models import BaseModel

EVENT_TYPES = [
    ("chat_message", "Chat Message"),
    ("new_group", "New Study Group"),
]


class Event(BaseModel):
    event_id = models.CharField(max_length=150, db_index=True)
    event_type = models.CharField(max_length=150, choices=EVENT_TYPES, blank=True, null=True, db_index=True)
    event_timestamp = models.DateTimeField(blank=True, null=True)
    creator = models.CharField(max_length=150, choices=EVENT_TYPES, blank=True, null=True, db_index=True)
    email = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    data = models.TextField(blank=True, null=True)


class PushTombstone(BaseModel):
    push_type = models.CharField(max_length=150)
    user_id = models.CharField(max_length=150)
    buid = models.CharField(max_length=150)
    event_id = models.CharField(max_length=150, db_index=True)
    tokens = models.TextField(blank=True, null=True)
    event = models.TextField(blank=True, null=True)


class EmailTombstone(BaseModel):
    user_id = models.CharField(max_length=150, db_index=True)
    buid = models.CharField(max_length=150, db_index=True)
    event_id = models.CharField(max_length=150, db_index=True)
    email = models.CharField(max_length=150, db_index=True)
    subject = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)


class GroupReminderTombstone(BaseModel):
    group_id = models.CharField(max_length=150, db_index=True)
    reminder_type = models.CharField(max_length=150, db_index=True)


class TimingTombstone(BaseModel):
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    difference = models.FloatField(blank=True, null=True)


class APITimingTombstone(BaseModel):
    response_time = models.FloatField(blank=True, null=True)
    success = models.BooleanField(default=False)


class PushTimingTombstone(BaseModel):
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    difference = models.FloatField(blank=True, null=True)
