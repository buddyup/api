from events.handlers.base import EventHandler
from gatekeeper.models import User
from gatekeeper.tasks import send_verification_email


class ResentVerifyEmailHandler(EventHandler):
    """Take care of all events and push event for resending the email verification."""

    event_types = ["resend_verification_email", ]

    def handle(self):
        user = User.objects.get(buid=self.cleaned_event["creator"])
        send_verification_email.delay(user.pk)
