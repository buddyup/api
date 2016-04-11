from events.handlers.base import EventHandler
from utils.school_data import school_data


class DevDatabaseResetHandler(EventHandler):
    """Take care of validating and resetting the developer database"""

    event_types = ["dev_database_reset", ]

    def handle(self):
        # NOTE: This overrides the entire database!
        # If you're copy/pasting for new events, don't copy/paste from here!
        self.put("/", self.dev_data)

    @property
    def dev_data(self):
        return {
            "dev": {
                "in_dev_mode": True,
                "last_reset_date": self.event["created_at"]
            },
            "users": {
                "user-3": {
                    "profile": {
                        "bio": "Sup campus?",
                        "first_name": "John",
                        "last_name": "Skelton"
                    }
                },
                "user-5": {
                    "news_feed": {
                        "-JpwmAazbeWOJbZcTmdu": {
                            "created_at": 1432317638108,
                            "creator": "user-5",
                            "data": {
                                "bio": "Hey. I'm cool",
                                "first_name": "Steven",
                                "full_name": "Steven Skoczen",
                                "last_name": "Skoczen",
                                "profile_pic": ""
                            },
                            "event_id": "-JpwmAazbeWOJbZcTmdu",
                            "full_name": "Steven Skoczen",
                            "involved": ["user-5", ],
                            "order": 8567682361892,
                            "profile_pic": "",
                            "type": "update_profile"
                        }
                    },
                    "profile": {
                        "bio": "Hey. I'm cool",
                        "first_name": "Steven",
                        "last_name": "Skoczen",
                        "profile_pic": "",
                    }
                }
            },
            "schools": {
                "hudson_edu": {
                    "profile": {
                        "name": "Hudson University",
                        "id": "hudson_edu",
                        "short_name": "Hudson",
                        "email_suffix": "hudson.edu",
                        "web_site": "www.buddyup.org",
                        "primary_color": "blue",
                        "secondary_color": "green",
                        "logo_full_url": "",
                        "logo_lg_url": "",
                        "logo_md_url": "",
                        "logo_sm_url": "",
                        "active": True,
                        "terms": {
                            "11235": {
                                "name": "Summer 2015",
                                "start": 1432317638108,
                                "end": 1432319638108,
                                "break_start": 1432317838108,
                                "break_end": 1432319798108,
                            }
                        }
                    },
                    "classes": {
                        "1389Y8": {
                            "order": 10,
                            "school_id": "hudson.edu",
                            "id": "1389Y8",
                            "subject_code": "CHEM",
                            "number": "101",
                            "name": "Intro to Chemistry",
                            "term_name": "Summer 2015",
                            "icon": "beaker",
                            "term_start_at": 1432317638108,
                            "term_end_at": 1432319638108
                        }
                    },
                    "groups": {}
                },
                "buddyup_org": {
                    "profile": {
                        "name": "BuddyUp University",
                        "id": "buddyup_org",
                        "short_name": "BU",
                        "email_suffix": "buddyup.org",
                        "web_site": "www.buddyup.org",
                        "primary_color": "blue",
                        "secondary_color": "green",
                        "logo_full_url": "",
                        "logo_lg_url": "",
                        "logo_md_url": "",
                        "logo_sm_url": "",
                        "active": True,
                        "terms": {
                            "11235": {
                                "id": "11235",
                                "name": "Summer 2015",
                                "start": 1432317638108,
                                "end": 1433319638108,
                                "break_start": 1432317838108,
                                "break_end": 1432319798108,
                            },
                            "11236": {
                                "id": "11236",
                                "name": "Fall 2015",
                                "start": 1532317638108,
                                "end": 1533319638108,
                                "break_start": 1532317838108,
                                "break_end": 1532319798108,
                            }
                        }
                    },
                    "classes": {
                        "1389Y8": {
                            "order": 10,
                            "school_id": "hudson.edu",
                            "id": "1389Y8",
                            "subject_code": "CHEM",
                            "number": "101",
                            "name": "Intro to Chemistry",
                            "term_name": "Summer 2015",
                            "icon": "beaker",
                            "term_start_at": 1432317638108,
                            "term_end_at": 1432319638108
                        }
                    },
                    "groups": {},
                    "subjects": {},
                }
            },
            "event_meta": {
                "-JpwmAazbeWOJbZcTmdu": {
                    "created_at": 1432317638108,
                    "creator": "user-5",
                    "data": {
                        "bio": "Hey. I'm cool",
                        "first_name": "Steven",
                        "full_name": "Steven Skoczen",
                        "last_name": "Skoczen",
                        "profile_pic": ""
                    },
                    "event_id": "-JpwmAazbeWOJbZcTmdu",
                    "full_name": "Steven Skoczen",
                    "involved": ["user-5", ],
                    "order": 8567682361892,
                    "profile_pic": "",
                    "type": "update_profile"
                }
            },
            "events": {
                "-JpwmAazbeWOJbZcTmdu": {
                    "created_at": 1432317638108,
                    "creator": "user-5",
                    "data": {
                        "bio": "Hey. I'm cool",
                        "first_name": "Steven",
                        "full_name": "Steven Skoczen",
                        "last_name": "Skoczen",
                        "profile_pic": ""
                    },
                    "event_id": "-JpwmAazbeWOJbZcTmdu",
                    "full_name": "Steven Skoczen",
                    "involved": ["user-5", ],
                    "order": 8567682361892,
                    "profile_pic": "",
                    "type": "update_profile"
                }
            }
        }
