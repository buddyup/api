from events.handlers.base import EventHandler


class DeviceInitHandler(EventHandler):
    """Take care of all events and push event for resending the email verification."""

    event_types = ["device_init", ]

    def handle(self):
        if (
            "device" in self.cleaned_event["data"] and
            "uuid" in self.cleaned_event["data"]["device"]
        ):
            device_id = self.cleaned_event["data"]["device"]["uuid"]
        else:
            device_id = self.cleaned_event["data"]["platform"]

        self.put("/users/%(creator)s/internal/devices/%(device_id)s" % {
            "creator": self.cleaned_event["creator"],
            "device_id": device_id,
        },
            self.cleaned_event["data"]
        )
