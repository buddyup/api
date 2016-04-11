from events.handlers.base import EventHandler
from tempfile import NamedTemporaryFile


class UpdateProfileHandler(EventHandler):
    """Take care of all events and push event for profile update changes"""

    event_types = ["update_profile", ]

    def handle(self):
        self.add_to_my_news_feed()
        self.add_to_buddies_news_feed()


class AccountCreationHandler(EventHandler):
    """Take care of all events and push events for user creating an account."""

    event_types = ["account_created", ]

    def handle(self):
        # Nothin, at present.
        pass


class SignupHandler(EventHandler):
    """Take care of all events and push event for a user signing up (finishing the welcome screen)."""

    event_types = ["signed_up", ]

    def handle(self):
        school_id = self.cleaned_event["data"]["school_id"]

        self.add_to_school(school_id)
        self.add_to_my_news_feed()
        self.add_to_buddies_news_feed()
        self.add_to_schoolmates_news_feed(school_id)
        self.increment("total_num_students")


class LoginHandler(EventHandler):
    """Take care of all events and push event for a user signing up (finishing the welcome screen)."""

    event_types = ["logged_in", ]

    def handle(self):
        # This gets auto-added to my events, and that's good enough.
        # self.reset_badge_count(self.cleaned_event["creator"])
        pass


class UpdateProfilePicHandler(EventHandler):
    """Take care of all events and push event for profile pic changes"""

    event_types = ["update_profile_pic", ]

    def handle(self):
        print("handling profile pic")
        from gatekeeper.models import User
        import base64
        import hashlib
        from io import BytesIO
        from PIL import Image
        from django.core.files.base import ContentFile

        # Process images.  Create thumbnails, save them to CDN, and return the url.
        pic = self.get_sync("users/%s/pictures" % self.cleaned_event["creator"])

        # pic["original"] is a large, 1200-wide png.
        pic_contents = base64.b64decode(
            pic["original"].split('base64,')[1]
        )

        user = User.objects.get(buid=self.cleaned_event["creator"])

        original_sha = hashlib.sha1(pic_contents).hexdigest()

        user.pic_original.save(
            "%s-original.png" % original_sha,
            ContentFile(pic_contents)
        )
        print(len(pic_contents))
        with NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(bytes(pic_contents))
            f.seek(0)
            # orig = Image.open(BytesIO(pic_contents))
            orig = Image.open(f.name)

            # .resize((width, height),
            medium = orig.resize((800, 800), Image.ANTIALIAS)
            medium_buffer = BytesIO()
            medium.save(medium_buffer, format="JPEG", quality=60)
            medium_buffer.seek(0)
            user.pic_medium.save(
                "%s-medium.jpg" % original_sha,
                ContentFile(medium_buffer.getvalue())
            )
            tiny = orig.resize((100, 100), Image.ANTIALIAS)
            tiny_buffer = BytesIO()
            tiny.save(tiny_buffer, format="JPEG", quality=60)
            tiny_buffer.seek(0)
            user.pic_tiny.save(
                "%s-tiny.jpg" % original_sha,
                ContentFile(tiny_buffer.getvalue())
            )
            user.save()

            self.put(
                "users/%s/public/profile_pic_url_medium" % self.cleaned_event["creator"],
                {".value": user.pic_medium.url}
            )
            self.put(
                "users/%s/public/profile_pic_url_tiny" % self.cleaned_event["creator"],
                {".value": user.pic_tiny.url}
            )
            print(user.pic_tiny.url)
        print("done")

    # self.add_to_my_news_feed()
    # self.add_to_buddies_news_feed()


class DeleteHandler(EventHandler):
    """Take care of all events and push events for user creating an account."""

    event_types = ["delete_account", ]

    def handle(self):
        # Confirm account is set to delete.
        u = self.get_sync("users/%s/marked_for_delete" % self.cleaned_event["creator"])
        if u is True:
            print("Delete confirmed")

        else:
            print("Error: Delete attempted for %s, but not marked for delete" % self.cleaned_event["creator"])
