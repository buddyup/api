import datetime
import inspect
import imp
import os
import time

from celery.task import task, periodic_task
from .helpers import MyEventHelpers, FriendEventHelpers, GroupEventHelpers,\
    ClassEventHelpers, SchoolEventHelpers, GlobalEventHelpers,\
    HeartEventHelpers, UserEventHelpers, AnalyticsHelpers

SYSTEM_CREATOR = "12391904!!! SYSTEM!! "


class EventHandler(
    MyEventHelpers, FriendEventHelpers, GroupEventHelpers,
    ClassEventHelpers, SchoolEventHelpers, GlobalEventHelpers,
    HeartEventHelpers, UserEventHelpers, AnalyticsHelpers
):

    def clean(self, event):
        """Cleans any sensitive data off the event."""
        cleaned = event
        if "key" in cleaned:
            del cleaned["key"]
        return cleaned

    def handle(self, event):
        """Routes the event to the right places. Overridden by all subclasses."""
        raise NotImplemented

    def __init__(self, event, *args, **kwargs):
        from events.tasks import firebase_put, firebase_get, firebase_delete, firebase_patch, push_and_email
        super(EventHandler, self).__init__(*args, **kwargs)
        self.event = event
        self.cleaned_event = self.clean(event)
        self.put = firebase_put.delay
        self.get = firebase_get.delay
        self.delete = firebase_delete.delay
        self.patch = firebase_patch.delay
        self.put_sync = firebase_put
        self.get_sync = firebase_get
        self.delete_sync = firebase_delete
        self.patch_sync = firebase_patch
        self.push_and_email = push_and_email.delay  # buid, data
        if "creator" in self.event and "event_id" in self.event and SYSTEM_CREATOR != self.event:
            self.add_to_user_events()


class AllEventHandlers(object):

    def __init__(self, *args, **kwargs):
        super(AllEventHandlers, self).__init__(*args, **kwargs)
        self.handlers = {}
        for root, dirs, files in os.walk(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "events",
            ),
            topdown=False
        ):
            for f in files:
                if f.endswith(".py") and f != "__init__.py" and f != "base.py":
                    module_path = os.path.join(root, f)
                    path_components = os.path.split(module_path)
                    module_name = path_components[-1][:-3]
                    # Need to pass along module name, path all the way through

                    mod = imp.load_source(module_name, module_path)
                    for class_name, cls in inspect.getmembers(mod, predicate=inspect.isclass):
                        if class_name != "EventHandler":
                            if not hasattr(cls, "event_types"):
                                print("Warning: %s has no event_types specified." % class_name)
                            else:
                                for event_type in cls.event_types:
                                    if event_type not in self.handlers:
                                        self.handlers[event_type] = []
                                    self.handlers[event_type].append(cls)

    @property
    def now(self):
        return int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
