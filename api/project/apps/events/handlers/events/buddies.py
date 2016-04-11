from events.handlers.base import EventHandler


class BuddiedUpHandler(EventHandler):
    """Take care of all events and push event for buddying up!"""

    event_types = ["buddied_up", ]

    def handle(self):

        requested_by = self.cleaned_event["data"]["requested_by"]
        accepted_by = self.cleaned_event["data"]["accepted_by"]

        # Add to requester's buddies
        url = "/users/%s/buddies/%s/" % (requested_by, accepted_by)
        self.put(url, {
            'user_id': accepted_by,
            'first_name': self.cleaned_event["first_name"],
            'last_name': self.cleaned_event["last_name"],
        })

        # Add to acceptor's buddies
        url = "/users/%s/buddies/%s/" % (accepted_by, requested_by)
        self.put(url, {
            'user_id': requested_by,
            'first_name': self.cleaned_event["data"]["requested_by_first_name"],
            'last_name': self.cleaned_event["data"]["requested_by_last_name"],
        })

        # Clear the request
        url = "/users/%s/buddy_requests/%s/" % (accepted_by, requested_by)
        self.delete(url)

        # In case of craziness w/ race conditions
        url = "/users/%s/buddy_requests/%s/" % (requested_by, accepted_by)
        self.delete(url)

        self.push_and_email(
            requested_by,
            "buddied_up",
            self.cleaned_event,
            badge_count=self.get_badge_count(requested_by),
        )

        # Tell all their buddies
        self.add_to_my_news_feed()
        self.add_to_user_news_feed(requested_by)
        self.add_to_users_buddies_news_feed(accepted_by)
        self.add_to_users_buddies_news_feed(requested_by)
        self.increment("total_buddy_matches")


class UnbuddiedHandler(EventHandler):
    """Take care of all events and push event for unbuddies"""

    event_types = ["unbuddied", ]

    def handle(self):

        requested_by = self.cleaned_event["data"]["requested_by"]
        accepted_by = self.cleaned_event["data"]["accepted_by"]

        # Add to requester's buddies
        url = "/users/%s/buddies/%s/" % (requested_by, accepted_by)
        self.delete(url)

        # Add to acceptor's buddies
        url = "/users/%s/buddies/%s/" % (accepted_by, requested_by)
        self.delete(url)

        self.decrement("total_buddy_matches")


class IgnoreRequestHandler(EventHandler):
    """Take care of all events and push event for ignored requests"""

    event_types = ["ignored_request", ]

    def handle(self):

        requested_by = self.cleaned_event["data"]["requested_by"]
        accepted_by = self.cleaned_event["data"]["accepted_by"]

        # # Add to requester's buddies
        url = "/users/%s/buddy_requests/%s/ignored" % (accepted_by, requested_by)
        self.put(url, {".value": True})

        #     {
        #     "ignored": True,
        #     "ignored_at": self.cleaned_event["created_at"]
        # })
        # self.delete(url)

        # # Add to acceptor's buddies
        # url = "/users/%s/buddies/%s/" % (accepted_by, requested_by)
        # self.delete(url)
        pass


class BuddyRequestHandler(EventHandler):
    """Take care of all events and push event for buddy requests"""

    event_types = ["buddy_request", ]

    def handle(self):
        # requested_by = self.cleaned_event["data"]["requested_by"]
        # requested_by_first_name = self.cleaned_event["data"]["requested_by_first_name"]
        # requested_by_last_name = self.cleaned_event["data"]["requested_by_last_name"]
        target_to = self.cleaned_event["data"]["target_to"]
        self.put("/users/%s/buddies-outgoing/%s" % (
            self.cleaned_event["creator"],
            target_to,
        ), {".value": True})

        self.increment_badge_count(target_to)

        self.push_and_email(
            target_to,
            "buddy_request",
            self.cleaned_event,
            badge_count=self.get_badge_count(target_to),
        )


class CancelBuddyRequestHandler(EventHandler):
    """Take care of all events and push event for cancelled buddy_requests"""

    event_types = ["cancel_buddy_request", ]

    def handle(self):
        target_to = self.cleaned_event["data"]["target_to"]
        self.delete("/users/%s/buddies-outgoing/%s" % (
            self.cleaned_event["creator"],
            target_to,
        ), {".value": True})
        pass


class BlockedUserHandler(EventHandler):
    """Take care of all events and push event for user blocks"""

    event_types = ["blocked", ]

    def handle(self):
        url = "/users/%s/internal/blocked_by/%s/" % (
            self.cleaned_event["data"]["target"],
            self.cleaned_event["creator"],
        )
        self.put(url, {".value": True})


class UnblockHandler(EventHandler):
    """Take care of all events and push event for unblocks"""

    event_types = ["unblocked", ]

    def handle(self):
        url = "/users/%s/internal/blocked_by/%s/" % (
            self.cleaned_event["data"]["target"],
            self.cleaned_event["creator"],
        )
        print(url)
        self.delete(url)
