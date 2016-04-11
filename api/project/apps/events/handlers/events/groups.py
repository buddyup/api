from events.handlers.base import EventHandler, SYSTEM_CREATOR
from events.models import GroupReminderTombstone


class CreateGroupHandler(EventHandler):
    """Take care of all events and push event for profile update changes"""

    event_types = ["created_group", ]

    def handle(self):
        from gatekeeper.tasks import notify_new_group

        # if (self.cleaned_event["data"]["subject"] != "open"):
        class_id = self.cleaned_event["data"]["subject"]
        self.add_to_class_news_feed(class_id)
        self.add_to_class_groups(class_id, self.cleaned_event["data"])

        # else:
        #     self.push_to_my_buddies(
        #         "my_groups",
        #     )

        school_id = self.cleaned_event["data"]["school_id"]
        self.add_to_school_groups(school_id, self.cleaned_event["data"])

        group_id = self.cleaned_event["event_id"]

        self.add_to_group_attending(group_id, self.cleaned_event["creator"])
        self.add_to_group_news_feed(group_id)
        self.add_to_buddies_news_feed()
        self.add_to_my_news_feed()
        self.increment("total_study_groups")
        # self.add_to_schoolmates_news_feed(school_id)

        # TODO: push?
        self.push_to_class(
            class_id,
            "classes",
        )
        notify_new_group(self.cleaned_event["creator"], self.cleaned_event)


class UpdatedGroupHandler(EventHandler):
    """Take care of all events and push event for profile update changes"""

    event_types = ["updated_group", ]

    def handle(self):
        group = self.get_sync("/groups/%s/" % self.cleaned_event["data"]["group_id"])
        self.patch(
            "/class/%s/groups/%s/" % (self.cleaned_event["data"]["subject"], self.cleaned_event["data"]["group_id"]),
            self.cleaned_event["data"]
        )
        if "attending" in group:
            for user_id, user_data in group["attending"].items():
                self.patch(
                    "/user/%s/groups/%s/" % (user_id, self.cleaned_event["data"]["group_id"]),
                    self.cleaned_event["data"]
                )


class AddGroupHandler(EventHandler):
    """Take care of all events and push event for group adds"""

    event_types = ["attending_group", ]

    def handle(self):
        if (self.cleaned_event["data"]["subject"] != "open"):
            class_id = self.cleaned_event["data"]["subject"]
            self.add_to_class_news_feed(class_id)

        group_id = self.cleaned_event["data"]["group_id"]

        self.add_to_group_attending(group_id, self.cleaned_event["creator"])
        self.add_to_group_news_feed(group_id)
        self.add_to_buddies_news_feed()
        self.add_to_my_news_feed()


class DropGroupHandler(EventHandler):
    """Take care of all events and push event for group drops"""

    event_types = ["cancel_group_attend", ]

    def handle(self):

        group_id = self.cleaned_event["data"]["group_id"]

        self.add_to_group_news_feed(group_id)
        self.remove_from_group_attending(group_id, self.cleaned_event["creator"])
        # self.add_to_buddies_news_feed()
        # self.add_to_my_news_feed()

        # We could, but I'm not conviced we should do anything quite yet.
        # self.add_to_group_news_feed()
        # self.add_to_buddies_news_feed()
        pass


class UpcomingGroupHandler(EventHandler):
    """Take care of sending pushes and news_feed updates for group is about to start"""
    # Note data comes from tasks.py
    # data = {
    #     "type": group_reminder,
    #     "group_id": group_id,
    #     "reminder_type": reminder_type,
    # }

    event_types = ["group_reminder", ]

    def handle(self):
        if self.cleaned_event["creator"] == SYSTEM_CREATOR:
            group = self.get_sync("/groups/%s/" % self.cleaned_event["group_id"])
            # Yep, this is hacky.
            group["event_id"] = self.cleaned_event["event_id"]
            group["type"] = "group_reminder"
            self.cleaned_event["group"] = {}
            self.cleaned_event["group"]["profile"] = group["profile"]

            if "attending" in group:
                self.cleaned_event["group"]["attending"] = group["attending"]
                for user_id, user_data in group["attending"].items():
                    self.add_to_user_news_feed(user_id)
                    self.push_and_email(user_id, "my_groups", group, push_type_values=["on", ])

            self.push_and_email(self.cleaned_event["creator"], "my_groups", group, push_type_values=["on", ])

            GroupReminderTombstone.objects.create(
                group_id=self.cleaned_event["group_id"],
                reminder_type=self.cleaned_event["reminder_type"],
            )
        else:
            print("Unauthorized")
