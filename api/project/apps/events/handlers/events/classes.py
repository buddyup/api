from events.handlers.base import EventHandler


class CreateClassHandler(EventHandler):
    """Take care of all events and push event for profile update changes"""

    event_types = ["created_class", ]

    def handle(self):
        from gatekeeper.tasks import notify_new_class

        self.add_to_buddies_news_feed()
        school_id = self.cleaned_event["data"]["school_id"]
        self.add_to_schoolmates_news_feed(school_id)
        class_id = self.cleaned_event["data"]["id"]
        self.add_to_class_news_feed(class_id)

        self.increment("total_classes")

        notify_new_class(self.cleaned_event["creator"], self.cleaned_event)


class AddClassHandler(EventHandler):
    """Take care of all events and push event for class adds"""

    event_types = ["added_class", ]

    def handle(self):
        self.add_to_my_news_feed()

        # Main event adds to /users/me/classes
        class_id = self.cleaned_event["data"]["course_id"]

        self.add_to_class_students(class_id)
        self.add_to_class_news_feed(class_id)
        self.add_to_buddies_news_feed()


class DropClassHandler(EventHandler):
    """Take care of all events and push event for class drops"""

    event_types = ["dropped_class", ]

    def handle(self):
        class_id = self.cleaned_event["data"]["course_id"]
        self.remove_from_class_students(class_id)

        # We could, but I'm not conviced we should do anything quite yet.
        # self.add_to_class_news_feed()
        # self.add_to_buddies_news_feed()
        pass
