# Buddyup Javascript API

## $scope.me

`$scope.me` contains all the user data, and events.  All data is read-only, and is modified by calling the appropriate event handler.

### Data

The tree of `$scope.me` is below.

- `agreed_to_terms` (boolean) -  Whether the user has agreed to the terms.
- `opt_in_to_school_updates` (boolean) - Whether the user has opted-in to recieving "BuddyUp is now at your school" emails.
- `first_name` (string) - User's first name.
- `last_name` (string) - User's last name.
- `bio` (string) - User's bio.
- `profile_pic_lg_url` (string) - Large profile picture, 1600xN.
- `profile_pic_md_url` (string) - Medium profile picture, 800xN.
- `profile_pic_sm_url` (string) - Small profile picture, 200xN.
- `profile_pic_full_url` (string) - Full size profile picture (original image, should be unused in app.)
- `primary_email` (string) - User's primary email address.
- `email_validated` (boolean) - Whether the user's email has been verified
- `blocked_users` (object):

    ```js
    {
        "1234": true,  # User 1234 has been blocked.
        "45670": false,  # User 45670 was blocked at some point, but has been unblocked by the user.
    }
    ```

- `profile` (private variable, do not use.)
- `buddies` (object):
    
    ```js
    {
        "123": {
            "first_name": "Sally",
            "last_name": "Williams",
            "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/123/profile_large.jpg",
            "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/123/profile_medium.jpg",
            "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/123/profile_small.jpg",
        },
        "456": {
            "first_name": "Jillian",
            "last_name": "Christopherson",
            "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
            "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
            "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
        }
    }
    ```

- `buddy_search`:
    - filter (object):  **Note** Unused for v1.0, subject to change.

        ```js
        {
            name: "",
            major: "",
            language: ""
        }
        ```

    - matches (object):  **Note**: Needs paging added.

        ```js
        {
            "123": {
                "first_name": "Sally",
                "last_name": "Williams",
                "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/123/profile_large.jpg",
                "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/123/profile_medium.jpg",
                "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/123/profile_small.jpg",
            },
            "456": {
                "first_name": "Jillian",
                "last_name": "Christopherson",
                "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
                "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
                "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
            }
        }
        ```

- `buddies_hearts` (object): List of hearts by my buddies, keyed by `heart_id`.  For each `heart_id`:
    
    - `user` (object): a public User object:
    
        ```js
        {
            "first_name": "Jillian",
            "last_name": "Christopherson",
            "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
            "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
            "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
        }
        ```

    - `user_id` (string): the user id of the person who made the heart
    - `object_uri` (string): the canonical firebase URL for the hearted object, i.e.  `"/news_feed_archive/123985123"`
    - `summary` (string): A summary of what was hearted.  i.e. "Sally Williams joined Chem 357",
    - `hearted_on` (number): Time the heart took place, in milliseconds since epoch.


- `classes` (object): List of the user's classes, keyed by `class_id`.  For each `class_id`:


    - `short_name` (string):  The class-listing name of the course, i.e. "Chem201".
    - `long_name` (string): The descriptive name of the course, i.e. "Organic Chemistry".
    - `term_name` (string): The course term, i.e. "Spring 2015".
    - `term_start` (number): The start date of the term, in ms since epoch.
    - `term_end` (number): The start date of the term, in ms since epoch.
    - `is_active` (string): Whether or not the class is currently active (updated nightly).
    - `classmates` (object): A list of classmates, keyed by `user_id`.  For each `user_id`:

        ```js
        {
            "mood": "confident",
            "profile": {
                "first_name": "Jillian",
                "last_name": "Christopherson",
                "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
                "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
                "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
            },
        }
        ```

    - `recent_messages` (object):  The last 200 chat messages for a class, keyed by `message_id`.  For each `message_id`,
        

        - `user_id` (string): Message sender's `user_id`.
        - `first_name` (string): Message sender's first name.
        - `last_name` (string): Message sender's last name
        - `profile_pic_lg_url` (string): "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
        - `profile_pic_md_url` (string): "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
        - `profile_pic_sm_url` (string): "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
        - `at` (string): 123657498461
        - `class` (string): "12456"
        - `text` (string): "Anyone want to hang out afterwards and review this part?  What's going on?"
        - `hearts` (object): List of hearts for this post, keyed by `heart_id`.  For each `heart_id`:

            - `user` (object): a public User object:
            
                ```js
                {
                    "first_name": "Jillian",
                    "last_name": "Christopherson",
                    "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
                    "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
                    "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
                }
                ```

            - `user_id` (string): the user id of the person who made the heart
            - `object_uri` (string): the canonical firebase URL for the hearted object, i.e.  `"/news_feed_archive/123985123"`
            - `summary` (string): A summary of what was hearted.  i.e. "Sally Williams joined Chem 357",
            - `hearted_on` (number): Time the heart took place, in milliseconds since epoch.
    
    - `groups` (object): All upcoming groups for a class, keyed by `group_id`.  For each `group_id`:

        - `creator` (string): Creator's information:
            
            ```js
            {
                "first_name": "Jillian",
                "last_name": "Christopherson",
                "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
                "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
                "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
            }
            ```

        - `location` (string): Where the study group is being held.
        - `start_time` (number): What time study group starts, in milliseconds since epoch.
        - `end_time` (number): What time study group ends, in milliseconds since epoch.
        - `max_number` (string): Maximum number of attendees
        - `attending` (object): List of users who are attending, keyed by `user_id`.  For each `user_id`:

            ```js
            {
                "first_name": "Jillian",
                "last_name": "Christopherson",
                "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
                "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
                "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
            }
            ```
            
        - `maybe` (object): List of users who are maybes, keyed by `user_id`.  For each `user_id`:
        
            ```js
            {
                "first_name": "Jillian",
                "last_name": "Christopherson",
                "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
                "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
                "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
            }
            ```
            
- `hearts` (object): a list of all the things a user has hearted, keyed by `heart_id`.  For each `heart_id`:


    - `user` (object): a public User object:

        ```js
        {
            "first_name": "Jillian",
            "last_name": "Christopherson",
            "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
            "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
            "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
        }
        ```

    - `user_id` (string): the user id of the person who made the heart
    - `object_uri` (string): the canonical firebase URL for the hearted object, i.e.  `"/news_feed_archive/123985123"`
    - `summary` (string): A summary of what was hearted.  i.e. "Sally Williams joined Chem 357",
    - `hearted_on` (number): Time the heart took place, in milliseconds since epoch.

- `news_feed_stories` (object): a list of the last 200 news feed stories for a user.  Keyed by `story_id`.  For each `story_id`:
    
    - `creator` (string): The user_id for the person who started the story.
    - `type` (string): The story type.
    - `data` (object): All necessary data to render that particular story type.
    - `hearts` (object): List of hearts for this story, keyed by `heart_id`.  For each `heart_id`:

        - `user` (object): a public User object:
        
            ```js
            {
                "first_name": "Jillian",
                "last_name": "Christopherson",
                "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
                "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
                "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
            }
            ```

        - `user_id` (string): the user id of the person who made the heart
        - `object_uri` (string): the canonical firebase URL for the hearted object, i.e.  `"/news_feed_archive/123985123"`
        - `summary` (string): A summary of what was hearted.  i.e. "Sally Williams joined Chem 357",
        - `hearted_on` (number): Time the heart took place, in milliseconds since epoch.

- `preferences` (object): The user's email and push notification preferences.

    - `email` (object): an dictionary of booleans, keyed by the option name.
    - `push` (object): an dictionary of booleans, keyed by the option name.

- `inbox`: The user's messages and pending buddy requests.
    - `num_unread` (number):  The total number of unread messages and unseen requests.
    - conversations (object): A list of conversations, keyed by `thread_id`.  For each `thread_id`:
        - `user` (object): a public User object:
        
            ```js
            {
                "first_name": "Jillian",
                "last_name": "Christopherson",
                "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
                "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
                "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
            }
            ```

        - messages:
            - `from` (string):  `user_id` for the sending user.
            - `to` (string):  `user_id` for the recipient (will always be me)
            - `text` (string): The message body.
            - `sent_at` (number): Time the send took place, in milliseconds since epoch.
            - `read` (boolean): If the message has been read.
            - `read_at` (number): Time the read took place, in milliseconds since epoch.

- `buddy_requests` (object):  The user's buddy requests.  Keyed by `relationship_id`.  For each `relationship_id`:
    - `from`: (string):  the `user_id` for the sending user.
    - `to`: (string):  the `user_id` for the recipient (will always be me)
    - `accepted`: (boolean):  if the request was accepted.
    - `accepted_on`: (number):  Time the acceptance took place, in milliseconds since epoch.
    - `viewed`: (boolean):  if the request was viewed.
    - `viewed_on`: (number):  Time the first view took place, in milliseconds since epoch.
    - `hidden`: (boolean): if the request was hidden (rejected).
    - `hidden_on`: (number): Time the hide took place, in milliseconds since epoch.


### Events

**Note**: Stubs are in, actual parameter specs are coming.

- `.read(data)`: The user read an object. Sends:
    
    ```js
    {
        "type": "private_message",  // news_item, chat_message
        "id": "12345"
    }

    ```

- `.viewed(data)`: 
    
    ```js
    {
        "type": "class",  // news_item, chat_message, group, 
        "id": "12345"
    }

    ```

- `.clicked(data)`: 
- `.update_profile(profile_data)`: 
- `.add_email(email_address)`: 
- `.remove_email(email_address)`: 
- `.set_primary_email(email_address)`: 
- `.update_notifications(notification_data)`: 
- `.send_validation_email()`: 
- `.mark_email_verified()`: 
- `.opt_in_to_school_updates()`: 
- `.agree_to_terms()`: 
- `.join_school(school_id)`: 
- `.leave_school(school_id)`: 
- `.join_class(class_id)`: 
- `.create_class(class_data)`: 
- `.leave_class(class_id)`: 
- `.set_mood(class_id)`: 
- `.archive_class(class_id)`: 
- `.create_group(study_data)`: 
- `.going_group(study_id)`: 
- `.maybe_group(study_id)`: 
- `.leave_group(study_id)`: 
- `.send_private_message(user_id, message)`: 
- `.send_chat_message(class_id, message)`: 
- `.viewed_private_message(message)`: 
- `.viewed_chat_message(message)`: 
- `.viewed_buddy_request(message)`: 
- `.send_buddy_request(user_id)`: 
- `.accept_buddy_request(user_id)`: 
- `.reject_buddy_request(user_id)`: 
- `.unbuddy(user_id)`: 
- `.block_user(user_id)`: 
- `.add_heart(heart_data)`: 
- `.remove_heart(heart_data)`: 
- `.report_content(content_data)`: 
- `.change_buddies_filter(filter_data)`: 
- `.delete_account()`: 
- `.push_notification(message)`: 

## $scope.get

`$scope.get` provides methods for getting a full object for a detailed, drill-down view of an object.

Methods at present:

- `$scope.get.user(user_id)` (object):
    
    - `first_name` (string) - User's first name.
    - `last_name` (string) - User's last name.
    - `bio` (string) - User's bio.
    - `profile_pic_lg_url` (string) - Large profile picture, 1600xN.
    - `profile_pic_md_url` (string) - Medium profile picture, 800xN.
    - `profile_pic_sm_url` (string) - Small profile picture, 200xN.
    - `profile_pic_full_url` (string) - Full size profile picture (original image, should be unused in app.)
    - `classes` (object): List of the user's classes, keyed by `class_id`.  For each `class_id`:

        - `short_name` (string):  The class-listing name of the course, i.e. "Chem201".
        - `long_name` (string): The descriptive name of the course, i.e. "Organic Chemistry".
        - `term_name` (string): The course term, i.e. "Spring 2015".
        - `term_start` (number): The start date of the term, in ms since epoch.
        - `term_end` (number): The start date of the term, in ms since epoch.
        - `is_active` (string): Whether or not the class is currently active (updated nightly).
        - `classmates` (object): A list of classmates, keyed by `user_id`.  For each `user_id`:

            ```js
            {
                "mood": "confident",
                "profile": {
                    "first_name": "Jillian",
                    "last_name": "Christopherson",
                    "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
                    "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
                    "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
                },
            }
            ```

        - `recent_messages` (object):  The last 200 chat messages for a class, keyed by `message_id`.  For each `message_id`,

            - `user_id` (string): Message sender's `user_id`.
            - `first_name` (string): Message sender's first name.
            - `last_name` (string): Message sender's last name
            - `profile_pic_lg_url` (string): "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
            - `profile_pic_md_url` (string): "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
            - `profile_pic_sm_url` (string): "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
            - `at` (string): 123657498461
            - `class` (string): "12456"
            - `text` (string): "Anyone want to hang out afterwards and review this part?  What's going on?"
            - `hearts` (object): List of hearts for this post, keyed by `heart_id`.  For each `heart_id`:

                - `user` (object): a public User object:
                
                    ```js
                    {
                        "first_name": "Jillian",
                        "last_name": "Christopherson",
                        "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
                        "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
                        "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
                    }
                    ```

                - `user_id` (string): the user id of the person who made the heart
                - `object_uri` (string): the canonical firebase URL for the hearted object, i.e.  `"/news_feed_archive/123985123"`
                - `summary` (string): A summary of what was hearted.  i.e. "Sally Williams joined Chem 357",
                - `hearted_on` (number): Time the heart took place, in milliseconds since epoch.

    - `buddies` (object):
        
        ```js
        {
            "123": {
                "first_name": "Sally",
                "last_name": "Williams",
                "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/123/profile_large.jpg",
                "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/123/profile_medium.jpg",
                "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/123/profile_small.jpg",
            },
            "456": {
                "first_name": "Jillian",
                "last_name": "Christopherson",
                "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
                "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
                "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
            }
        }
        ```

- `$scope.get.class(class_id)` (object):

    - `short_name` (string):  The class-listing name of the course, i.e. "Chem201".
    - `long_name` (string): The descriptive name of the course, i.e. "Organic Chemistry".
    - `term_name` (string): The course term, i.e. "Spring 2015".
    - `term_start` (number): The start date of the term, in ms since epoch.
    - `term_end` (number): The start date of the term, in ms since epoch.
    - `is_active` (string): Whether or not the class is currently active (updated nightly).
    - `classmates` (object): A list of classmates, keyed by `user_id`.  For each `user_id`:

        ```js
        {
            "mood": "confident",
            "profile": {
                "first_name": "Jillian",
                "last_name": "Christopherson",
                "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
                "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
                "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
            },
        }
        ```

    - `recent_messages` (object):  The last 200 chat messages for a class, keyed by `message_id`.  For each `message_id`,
        

        - `user_id` (string): Message sender's `user_id`.
        - `first_name` (string): Message sender's first name.
        - `last_name` (string): Message sender's last name
        - `profile_pic_lg_url` (string): "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
        - `profile_pic_md_url` (string): "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
        - `profile_pic_sm_url` (string): "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
        - `at` (string): 123657498461
        - `class` (string): "12456"
        - `text` (string): "Anyone want to hang out afterwards and review this part?  What's going on?"
        - `hearts` (object): List of hearts for this post, keyed by `heart_id`.  For each `heart_id`:

            - `user` (object): a public User object:
            
                ```js
                {
                    "first_name": "Jillian",
                    "last_name": "Christopherson",
                    "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
                    "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
                    "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
                }
                ```

            - `user_id` (string): the user id of the person who made the heart
            - `object_uri` (string): the canonical firebase URL for the hearted object, i.e.  `"/news_feed_archive/123985123"`
            - `summary` (string): A summary of what was hearted.  i.e. "Sally Williams joined Chem 357",
            - `hearted_on` (number): Time the heart took place, in milliseconds since epoch.

- `$scope.get.group(group_id)` (object): 
    
    - `creator` (string): Creator's information:
        
        ```js
        {
            "first_name": "Jillian",
            "last_name": "Christopherson",
            "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
            "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
            "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
        }
        ```

    - `location` (string): Where the study group is being held.
    - `start_time` (number): What time study group starts, in milliseconds since epoch.
    - `end_time` (number): What time study group ends, in milliseconds since epoch.
    - `max_number` (string): Maximum number of attendees
    - `attending` (object): List of users who are attending, keyed by `user_id`.  For each `user_id`:

        ```js
        {
            "first_name": "Jillian",
            "last_name": "Christopherson",
            "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
            "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
            "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
        }
        ```
        
    - `maybe` (object): List of users who are maybes, keyed by `user_id`.  For each `user_id`:
    
        ```js
        {
            "first_name": "Jillian",
            "last_name": "Christopherson",
            "profile_pic_lg_url": "https://aws.amazon.com/buddyup-core/users/456/profile_large.jpg",
            "profile_pic_md_url": "https://aws.amazon.com/buddyup-core/users/456/profile_medium.jpg",
            "profile_pic_sm_url": "https://aws.amazon.com/buddyup-core/users/456/profile_small.jpg",
        }
        ```

