class MyEventHelpers(object):

    def add_to_my_news_feed(self):
        # url = "/users/%(creator)s/news_feed/%(event_id)s" % self.event
        # self.put(url, self.cleaned_event)
        pass

    def add_to_my_hearts(self):
        # event_creator = self.event["data"]["event_data"]["creator"]
        # heart_user = self.event["creator"]
        # self.put('/users/%(creator)s/my_hearts/%(target_event_id)s' % {
        #     'creator': event_creator,
        #     'target_event_id': self.event["event_id"],
        # }, self.cleaned_event)

        # vals = ["everyone"]

        # url = "/users/%s/buddies/%s" % (heart_user, event_creator)
        # buddy = self.get_sync(url)
        # if (buddy):
        #     vals.append("buddies")
        pass

        # TODO: get smarter later.
        # self.push_and_email(
        #     event_creator,
        #     "hearts",
        #     self.cleaned_event,
        #     push_type_values=vals,
        #     badge_count=self.get_badge_count(event_creator),
        # )

    def remove_from_my_hearts(self):
        url = '/users/%(creator)s/my_hearts/' % {
            'creator': self.event["data"]["event_data"]["creator"],
        }

        l = self.get_sync(url)
        if not l:
            return {}

        target_event = self.cleaned_event["data"]["event_data"]["event_id"]

        for heart_event_id, heart_data in l.items():
            if heart_data["data"]["event_data"]["event_id"] == target_event:
                self.delete('/users/%(creator)s/my_hearts/%(heart_event_id)s' % {
                    'creator': self.event["data"]["event_data"]["creator"],
                    'heart_event_id': heart_event_id,
                })
                return


class UserEventHelpers(object):

    def add_to_user_events(self):
        # TODO: if I need this, write it, and include it.
        url = "/users/%(creator)s/events/%(event_id)s" % self.event
        self.put(url, self.cleaned_event)


class FriendEventHelpers(object):

    def user_buddy_list(self, user_id):
        url = "/users/%s/buddies/" % (user_id,)

        l = self.get_sync(url)
        if not l:
            return {}
        return l

    @property
    def my_buddy_list(self):
        return self.user_buddy_list(self.event["creator"])

    def add_to_buddies_news_feed(self):
        # for buddy_id, buddy_data in self.my_buddy_list.items():
        #     url = "/users/%s/news_feed/%s" % (
        #         buddy_id,
        #         self.cleaned_event["event_id"],
        #     )
        #     print("adding to %s news feed" % buddy_id)
        #     self.put(url, self.cleaned_event)
        pass

    def add_to_user_news_feed(self, user_id):
        # url = "/users/%s/news_feed/%s" % (
        #     user_id,
        #     self.cleaned_event["event_id"],
        # )
        # self.put(url, self.cleaned_event)
        pass

    def add_to_users_buddies_news_feed(self, user_id):
        # for buddy_id, buddy_data in self.user_buddy_list(user_id).items():
        #     self.add_to_user_news_feed(buddy_id)
        pass

    def add_to_my_buddies_hearts(self):
        # for buddy_id, buddy_data in self.my_buddy_list.items():
        #     if (self.event["data"]["event_data"]["creator"] != buddy_id):
        #         url = "/users/%(buddy_id)s/buddies_hearts/%(event_id)s" % {
        #             "buddy_id": buddy_id,
        #             "event_id": self.cleaned_event["event_id"],
        #         }
        #         self.put(url, self.cleaned_event)
        pass

    def remove_from_my_buddies_hearts(self):
        # for buddy_id, buddy_data in self.my_buddy_list.items():
        #     url = '/users/%(buddy_id)s/buddies_hearts/' % {
        #         'buddy_id': buddy_id,
        #     }

        #     l = self.get_sync(url)
        #     if not l:
        #         return {}

        #     target_event = self.cleaned_event["data"]["event_data"]["event_id"]
        #     for heart_event_id, heart_data in l.items():
        #         if (heart_data["data"]["event_data"]["creator"] != buddy_id):
        #             if heart_data["data"]["event_data"]["event_id"] == target_event:
        #                 self.delete('/users/%(creator)s/buddies_hearts/%(heart_event_id)s' % {
        #                     'creator': buddy_id,
        #                     'heart_event_id': heart_event_id,
        #                 })
        #                 return
        pass

    def push_to_user_buddies(self, user_id, push_type):
        for buddy_id, buddy_data in self.user_buddy_list(user_id).items():
            self.increment_badge_count(user_id)
            vals = ["everyone", "buddies"]

            # TODO: get smarter later.
            self.push_and_email(
                buddy_id,
                push_type,
                self.cleaned_event,
                push_type_values=vals,
                badge_count=self.get_badge_count(buddy_id),
            )

    def push_to_my_buddies(self, push_type):
        return self.push_to_user_buddies(
            self.cleaned_event["creator"], push_type
        )


class GroupEventHelpers(object):

    def groupmates(self, group_id):
        url = "/groups/%s/attending/" % (group_id,)

        l = self.get_sync(url)
        if not l:
            return {}
        return l

    def add_to_group_news_feed(self, group_id):
        print("adding to %s" % group_id)
        url = "/groups/%s/news_feed/%s/" % (
            group_id,
            self.cleaned_event["event_id"],
        )
        self.put(url, self.cleaned_event)

    def remove_from_group_news_feed(self, group_id):
        url = "/groups/%s/news_feed/%s/" % (
            group_id,
            self.cleaned_event["event_id"],
        )
        self.put(url, self.cleaned_event)

    def add_to_group_attending(self, group_id, user_id):
        url = "/groups/%s/attending/%s/" % (
            group_id,
            user_id,
        )
        self.put(url, {'.value': True})

    def remove_from_group_attending(self, group_id, user_id):
        url = "/groups/%s/attending/%s/" % (
            group_id,
            user_id,
        )
        self.delete(url)

    def push_to_group(self, group_id, push_type):
        event_creator = self.event["creator"]
        for user_id, user_data in self.groupmates(group_id).items():
            if event_creator != user_id:
                vals = ["everyone"]
                self.increment_badge_count(user_id)

                url = "/users/%s/buddies/%s" % (user_id, event_creator)
                buddy = self.get_sync(url)
                if (buddy):
                    vals.append("buddies")

                # TODO: get smarter later.

                self.push_and_email(
                    user_id,
                    push_type,
                    self.cleaned_event,
                    push_type_values=vals,
                    badge_count=self.get_badge_count(event_creator),
                )


class ClassEventHelpers(object):

    def classmates(self, class_id):
        url = "/classes/%s/students/" % (class_id,)

        l = self.get_sync(url)
        if not l:
            return {}
        return l

    def add_to_class_news_feed(self, class_id):
        url = "/classes/%s/news_feed/%s/" % (
            class_id,
            self.cleaned_event["event_id"],
        )
        self.put(url, self.cleaned_event)

    def add_to_class_students(self, class_id):
        url = "/classes/%(class_id)s/students/%(user_id)s" % {
            "class_id": class_id,
            "user_id": self.cleaned_event["creator"]
        }
        self.put(url, True)

    def remove_from_class_students(self, class_id):
        url = "/classes/%(class_id)s/students/%(user_id)s" % {
            "class_id": class_id,
            "user_id": self.cleaned_event["creator"]
        }
        self.delete(url)

    def add_to_class_groups(self, class_id, data):
        url = "/classes/%(class_id)s/groups/%(event_id)s" % {
            "class_id": class_id,
            "event_id": self.cleaned_event["event_id"],
        }
        self.put(url, data)

    def push_to_class(self, class_id, push_type):
        event_creator = self.event["creator"]
        for user_id, user_data in self.classmates(class_id).items():
            if event_creator != user_id:
                vals = ["everyone"]
                self.increment_badge_count(user_id)

                url = "/users/%s/buddies/%s" % (user_id, event_creator)
                buddy = self.get_sync(url)
                if (buddy):
                    vals.append("buddies")

                # TODO: get smarter later.

                self.push_and_email(
                    user_id,
                    push_type,
                    self.cleaned_event,
                    push_type_values=vals,
                    badge_count=self.get_badge_count(event_creator),
                )

    # def set_my_classmates(self):
    #     Don't know if we need this.
    #     pass


class SchoolEventHelpers(object):

    def my_schoolmates(self, school_id):
        url = "/schools/%s/students/" % school_id
        l = self.get_sync(url)
        if not l:
            return {}
        return l

    def add_to_school(self, school_id):
        url = "/schools/%(school_id)s/students/%(creator)s/" % {
            "school_id": school_id,
            "creator": self.cleaned_event["creator"],
        }
        self.put(url, True)

    def remove_from_school(self, school_id):
        url = "/schools/%(school_id)s/students/%(creator)s/" % {
            "school_id": school_id,
            "creator": self.cleaned_event["creator"],
        }
        self.delete(url)

    def add_to_schoolmates_news_feed(self, school_id):
        # for buddy_id, buddy_data in self.my_schoolmates(school_id).items():
        #     url = "/users/%(user_id)s/news_feed/%(event_id)s" % {
        #         "user_id": buddy_id,
        #         "event_id": self.cleaned_event["event_id"],
        #     }
        #     self.put(url, self.cleaned_event)
        pass

    def add_to_school_groups(self, school_id, data):
        url = "/schools/%(school_id)s/groups/%(event_id)s" % {
            "school_id": school_id,
            "event_id": self.cleaned_event["event_id"],
        }
        self.put(url, data)


class GlobalEventHelpers(object):

    def reset_badge_count(self, user_id):
        self.put(
            "users/%s/private/badge_count" % user_id,
            {".value": 0}
        )

    def get_badge_count(self, user_id):
        val = self.get_sync("users/%s/private/badge_count" % user_id)
        if not val:
            val = 0
        # print("val")
        print("badge count: %s" % val)
        return val

    def increment_badge_count(self, user_id):
        val = self.get_badge_count(user_id)

        self.put_sync(
            "users/%s/private/badge_count" % user_id,
            {".value": val + 1}
        )


class HeartEventHelpers(object):

    def update_event_heart(self):
        # Updates the heart count for the event everywhere it lives.

        # The User's news feed
        # url = "/users/%(user_id)s/news_feed/%(target_event_id)s/my_hearts/%(event_id)s" % {
        #     "user_id": self.cleaned_event["creator"],
        #     "target_event_id": self.cleaned_event["data"]["event_id"],
        #     "event_id": self.cleaned_event["event_id"],
        # }
        # self.put(url, self.cleaned_event)

        pass
        # The User's buddies news feeds
        # Class news feeds
        # Sesh news feeds


class AnalyticsHelpers(object):

    def increment(self, measure, count=1):
        # Updates the heart count for the event everywhere it lives.

        # The User's news feed
        url = "/analytics/%s" % measure

        starting_val = self.get_sync(url)
        # print(starting_val)
        new_val = starting_val + 1

        self.put_sync(url, {".value": new_val})

    def decrement(self, measure, count=1):
        # Updates the heart count for the event everywhere it lives.

        # The User's news feed
        url = "/analytics/%s" % measure

        starting_val = self.get_sync(url)
        # print(starting_val)
        new_val = starting_val - 1
        if new_val < 0:
            new_val = 0

        self.put_sync(url, {".value": new_val})
