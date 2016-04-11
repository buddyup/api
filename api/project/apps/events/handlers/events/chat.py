import json
import requests
from events.handlers.base import EventHandler
from django.conf import settings


class ChatMessageHandler(EventHandler):
    """Take care of all events and push event for class chat messages"""

    event_types = ["chat_message", ]

    def handle(self):
        # It's already been added to class/123/news_feed.

        # Nothing more, yet.
        if "class_id" in self.cleaned_event["data"]:
            class_id = self.cleaned_event["data"]["class_id"]
            self.push_to_class(class_id, "classes")

        elif "group_id" in self.cleaned_event["data"]:
            # TOOD: push to group
            group_id = self.cleaned_event["data"]["group_id"]
            self.push_to_group(group_id, "my_groups")


class ReportedMessageHandler(EventHandler):
    """Take care of all events and push events reported content"""

    event_types = ["report_content", ]

    def handle(self):
        url = "/reported/%(event_id)s/%(reporter)s" % {
            "event_id": self.cleaned_event["data"]["event_id"],
            "reporter": self.cleaned_event["creator"],
        }
        self.put(url, self.cleaned_event)

        # TODO: notify us if a certain threshold is hit (>1, etc.) We need a policy for this.
        try:
            print("%s/api/reported" % settings.WILL_URL)
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(
                "%s/api/reported" % settings.WILL_URL,
                headers=headers,
                data=json.dumps(self.cleaned_event)
            )
            assert r.status_code == 200
        except:
            print(r.status_code)
            print(r.json())
            import traceback
            traceback.print_exc()


class ReportedCancelledMessageHandler(EventHandler):
    """Take care of all events and push events reported content cancelled"""

    event_types = ["cancel_report_content", ]

    def handle(self):
        url = "/reported/%(event_id)s/%(reporter)s" % {
            "event_id": self.cleaned_event["data"]["event_id"],
            "reporter": self.cleaned_event["creator"],
        }
        self.delete(url)

        # TODO: notify us if a certain threshold is hit (>1, etc.) We need a policy for this.
        try:
            print("%s/api/cancel-report" % settings.WILL_URL)
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(
                "%s/api/cancel-report" % settings.WILL_URL,
                headers=headers,
                data=json.dumps(self.cleaned_event)
            )
            assert r.status_code == 200
        except:
            import traceback
            traceback.print_exc()


class ThreadCreatedHandler(EventHandler):
    """Take care of all events and push event for thread being created"""

    event_types = ["thread_created", ]

    def handle(self):
        pass

        # Still debating on this, but for the moment, not doing anything.

        # Update inbox for sender
        # thread_info = {
        #     "order": self.cleaned_event["order"],
        #     "with": {
        #         "user_id": self.cleaned_event["data"]["recipient"],
        #         "first_name": self.cleaned_event["data"]["recipient_first_name"],
        #         "last_name": self.cleaned_event["data"]["recipient_last_name"],
        #     },
        #     "last_message_at": self.cleaned_event["created_at"],
        #     "last_message_body": self.cleaned_event["data"]["body"],
        #     "user_id": self.cleaned_event["creator"],
        #     "thread_id": self.cleaned_event["data"]["thread_id"],
        # }

        # url = "/users/%(sender)s/inbox/%(recipient)s/" % self.cleaned_event["data"]
        # self.put(url, thread_info)


class PrivateMessageHandler(EventHandler):
    """Take care of all events and push event for message being sent"""

    event_types = ["private_message", ]

    def handle(self):
        # Update inbox for sender
        # url = "/users/%(sender)s/inbox/%(recipient)s/last_message_body" % self.cleaned_event["data"]
        # self.put(url, {".value": self.cleaned_event["data"]["body"]})

        # url = "/users/%(sender)s/inbox/%(recipient)s/last_message_at" % self.cleaned_event["data"]
        # self.put(url, {".value": self.cleaned_event["created_at"]})
        thread_info = {
            "order": self.cleaned_event["order"],
            "with": {
                "user_id": self.cleaned_event["data"]["recipient"],
                "first_name": self.cleaned_event["data"]["recipient_first_name"],
                "last_name": self.cleaned_event["data"]["recipient_last_name"],
            },
            "last_message_at": self.cleaned_event["created_at"],
            "last_message_body": self.cleaned_event["data"]["body"],
            "user_id": self.cleaned_event["data"]["recipient"],
            "thread_id": self.cleaned_event["data"]["thread_id"],
        }

        url = "/users/%(sender)s/inbox/%(recipient)s/" % self.cleaned_event["data"]
        self.put(url, thread_info)

        # Update inbox for recipient
        # Full update, so we don't start a thread in another user's inbox before a message has been sent.
        recipient_thread_info = {
            "order": self.cleaned_event["order"],
            "with": {
                "user_id": self.cleaned_event["data"]["sender"],
                "first_name": self.cleaned_event["data"]["sender_first_name"],
                "last_name": self.cleaned_event["data"]["sender_last_name"],
            },
            "last_message_at": self.cleaned_event["created_at"],
            "last_message_body": self.cleaned_event["data"]["body"],
            "user_id": self.cleaned_event["data"]["sender"],
            "thread_id": self.cleaned_event["data"]["thread_id"],
        }
        url = "/users/%(recipient)s/inbox/%(sender)s/" % self.cleaned_event["data"]
        self.put(url, recipient_thread_info)

        self.increment_badge_count(self.cleaned_event["data"]["recipient"])
        self.push_and_email(
            self.cleaned_event["data"]["recipient"],
            "private_message",
            self.cleaned_event,
            badge_count=self.get_badge_count(self.cleaned_event["data"]["recipient"]),
        )
