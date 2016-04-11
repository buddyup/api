from events.handlers.base import EventHandler


class HeartHandler(EventHandler):
    """Take care of all events and push event for hearting an event"""

    event_types = ["heart", ]

    def handle(self):

        if self.cleaned_event["data"]["on"]:
            self.add_to_my_hearts()
            self.add_to_my_buddies_hearts()
        else:
            self.remove_from_my_hearts()
            self.remove_from_my_buddies_hearts()
