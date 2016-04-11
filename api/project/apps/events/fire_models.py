class FirebaseModel(object):
    def save(self, ):
        # Turn self. kwargs (cleaned) into data, save to fb.
        pass


class UserEvents(FirebaseModel):

    def read(self, data):
        # User read a particular news feed story
        # triggered on scroll
        pass

    def viewed(self, data):
        # User viewed a particular item
        pass

    def clicked(self, data):
        # User clocked on a particular item
        pass

    def update_profile(self, profile_data):
        pass

    def add_email(self, email_address):
        pass

    def remove_email(self, email_address):
        pass

    def set_primary_email(self, email_address):
        pass

    def update_notifications(self, notification_data):
        pass

    def send_validation_email(self):
        pass

    def mark_email_verified(self):
        pass

    def opt_in_to_school_updates(self):
        pass

    def agree_to_terms(self):
        pass

    def join_school(self, school_id):
        pass

    def leave_school(self, school_id):
        pass

    def join_class(self, class_id):
        pass

    def create_class(self, class_data):
        pass

    def leave_class(self, class_id):
        pass

    def set_mood(self, class_id):
        pass

    def archive_class(self, class_id):
        pass

    def create_group(self, study_data):
        pass

    def going_group(self, study_id):
        # Adds me to sesh.going
        # Adds sesh to me/sesh/
        pass

    def leave_group(self, study_id):
        pass

    def send_private_message(self, user_id, message):
        pass

    def send_chat_message(self, class_id, message):
        pass

    def viewed_private_message(self, message):
        pass

    def viewed_chat_message(self, message):
        pass

    def viewed_buddy_request(self, message):
        pass

    def send_buddy_request(self, user_id):
        pass

    def accept_buddy_request(self, user_id):
        pass

    def reject_buddy_request(self, user_id):
        pass

    def unbuddy(self, user_id):
        pass

    def block_user(self, user_id):
        pass

    def add_heart(self, heart_data):
        pass

    def remove_heart(self, heart_data):
        pass

    def report_content(self, content_data):
        pass

    def change_buddies_filter(self, filter_data):
        pass

    def delete_account(self):
        pass

    # Maybe in a different place
    def push_notification(self, message):
        pass


class UserProperties(FirebaseModel):
    pass
    # # Actually, JS-only, but for now:
    # scope.me
    #     .events.foo()
    #     .readonly
    #         - agreed_to_terms: {object: boolean}
    #         - opt_in_to_school_updates: {object: boolean}
    #         - first_name: {type: string}
    #         - last_name: {type: string}
    #         - bio: {type: string}
    #         - profile_pic_lg_url: {type: string}
    #         - profile_pic_md_url: {type: string}
    #         - profile_pic_sm_url: {type: string}
    #         - profile_pic_full_url: {type: string}
    #         - primary_email: {type: string}
    #         - email_verified: {type: boolean}
    #         - blocked_users: {type: object}  # key is uid, val is true/false
    #         - profile (not exposed)
    #             - public
    #             - private
    #         - buddies/user_id
    #         - buddy_search:
    #             - filter: {type: object}
    #             - matches/user_id
    #         - buddies_hearts/heart_id
    #                 user: {$ref: "#/definitions/User"}
    #                 object_uri: {type: string}
    #                 summary: {type: string}
    #                 hearted_on: {type: number}
    #         - classes/class_id:
    #                 short_name: {type: string}
    #                 long_name: {type: string}
    #                 term_name: {type: string}
    #                 term_start: {type: number}
    #                 term_end: {type: number}
    #                 classmates/user_id
    #                     profile: {$ref: "#/definitions/User"}
    #                     status: {type: string}
    #                 recent_messages/message_id  # Last 200 messages
    #                     from: {type: string}  # user_id
    #                     at: {type: number}
    #                     class: {type: string}  # class_id
    #                     text: {type: string}
    #                     hearts/heart_id
    #                         {$ref: "#/definitions/Heart"}
    #         - hearts/heart_id
    #             {$ref: "#/definitions/Heart"}

    #         - news_feed_stories/story_id:   # Last 200 stories
    #             creator: {type: string}
    #             type: {type: string}
    #             data: {type: object}
    #             hearts:
    #                     constraint: false
    #                     type: object
    #                     additionalProperties: false
    #                     $heart_id: {$ref: "#/definitions/Heart"}
    #         - preferences:
    #             email: {}
    #             push: {}
    #         - inbox:
    #             num_unread: {type: number}
    #             conversations/message_id:
    #                 from: {type: string}  # uid
    #                 to: {type: string}  # uid
    #                 text: {type: string}
    #                 read: {type: boolean}
    #                 read_at: {type: number}

    #         - buddy_requests:
    #             from: {type: string}
    #             to: {type: string}
    #             accepted: {type: boolean}
    #             accepted_on: {type: number}
    #             viewed: {type: boolean}
    #             viewed_on: {type: number}
    #             hidden: {type: boolean}
    #             hidden_on: {type: number}


class StaffEvents(FirebaseModel):

    def add_school(self, data):
        pass

    def update_school(self, data):
        pass

    # Is this possible?
    # def delete_school(self, data):
    #     pass


class School(FirebaseModel):
    pass


class Class(FirebaseModel):
    @property
    def is_active(self):
        pass


class StudyGroup(FirebaseModel):
    @property
    def is_full(self):
        pass


class ChatMessage(FirebaseModel):
    pass


class PrivateMessage(FirebaseModel):
    pass


class BuddyRequest(FirebaseModel):
    pass


class Heart(FirebaseModel):
    pass
