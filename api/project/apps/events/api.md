
Big Big picture:
=====================
Everything is archived in postgres.  Just keep relevant stuff in firebase.  No archiving.
=====================


Separation:
Client:
1. Updates the canonical copy
2. Sends an event to the API.

Server:
3. Logs events
4. Copies events (minus any sensitive data) into indexed copies.

Heart (Dumbest thing I can think of):
    1. Client updates the exact event they're looking at
    2. Server updates events everywhere they live (based on parent event)
        - event goes in:
            - /events (?)
            - /user/creator/event
            - /user/news_feed/event (if in news feed)
            - /class/1/events
            - /sesh/1/events
            - for each of my friends
                - /user/1/news_feed (and aggregates)
    3. Server updates
        - /user/1/my_hearts
        - for each of my friends
            - /user/1/buddies_hearts (and aggregates)

K. 


## Client is bound to:

Wires up api that lives under scope.me.
Rule - anything we're doing sorting on the server (rule of thumb:
if it needs limiting) we make a separate connection for.
Every root node in the list below is bound.
- me.news_feed = []
- me.public
    - first_name
    - last_name

    - .buddies = [{public profile}]
    - .classes = [id, id]
    - .groups = [id, id]
    - .schools = [id,]
    - .inbox = [{with_profile_info, messaage_id, last_update, read}, ]
me.last_reads
    - .home = timestamp
    - .classes = timestamp
    - .groups = timestamp
    - .buddies = timestamp
    - .hearts = timestamp
    - .inbox = timestamp
    - .profile = timestamp
    - .class_details = {
        123: timestamp
      }
    - .group_details = {
        123: timestamp
      }
    watch on this ^, update new_messages object on change
- me.inbox[1]
       - .messages = []
           -. when we update a thread, update the last_message_timestamp
- me.buddy_requests = []
- me.my_hearts = []
- me.buddies_hearts = []
- me.classes[1].news_feed = []
- me.classes[1].new_messages = [] (.orderByChild('order').startAt(me.public.last_reads.class_details[1]))
- me.classes[1].groups = []
- me.classes[1].profile
    - .info = {}
    - .classmates = []
- me.groups[0].news_feed = []
- me.groups[0].profile
- me.groups[0].new_messages = [] (.orderByChild('order').startAt(me.public.last_reads.class_details[1]))
- me.schools[0].groups = []
- me.schools[0].profile


## Server

```
/user/1 (this node is never bound to)
  - profile = {
      - public {
        - first_name
      }
      - private {
        - last_reads = {}
        - settings = {}
      }
    }
  - buddy
       /user2
           /first_name

  - buddy_requests
       /user3
           /profile
           /time
  - event = []  (never used in app, just grouncontrold)
  - my_hearts = [ everything to render my hearts list. ]
  - buddies_hearts = [ everything to render buddies hearts list]
  - classes = [
    class_id: {
      - name
      - course_number
      - icon
      - last_changed
    },
  ]
  - groups = []
  - schools = []
  - inbox = [
    message_id: {
        with_user_profile_info,
        message_thread_id,
        last_update,
        read
    },
  ]
  - news_feed = []
/message_thread/1
      info
        - sender
        - recipient
        - last_message
      messages = []
/class
/group
/school
/event
    /1
       .hearts = {userid: true}
       .comments = []
```

? who can view this?

No rendering of events happens anywhere but 


Event
"Event is a public expression of something that happened"
    type: enum
    creator: string, uid
    created_at: timestamp
    involved: [uid, uid]
    data: {}
    visible_to: enum: [public, buddies]
    first_name:
    last_name:
    full_name:
    


types: onetoonemessage, chatmessage, attendance_change, join_class, leave_class, heart, unheart, sesh_starting
buddied_up, updated_profile, updated_picture




## Older thoughts:

Questions:
    - do we care about unread in news feed?  yes, for emails, someday.

Events:
User/uid/news_feed/notice_id
User/uid/my_hearts/notice_id
User/uid/buddies_hearts/notice_id

unread from the app's point of view is:

news_feed_read_at: timestamp
hearts_read_at: timestamp
class/classid/read_at: timestamp
sesh/seshid/read_at: timestamp

Normalized, Canonical:
/user/uid/events/id
/school/schid/class/classid/events/id
/school/schid/sesh/seshid/events/id


Lose easily: the ability to know which messages I've read.
    Can get back with: just keep ids in read/unread.  Not easy, but possible.
Gain: data's not in 500 places.


Class/events/id
    /termid
Sesh/events/id
    /going
groundcontrol/events/id
groundcontrol/school/id/events/id
groundcontrol/user/id/events/id

Undecided: are these events?
Messages:
1-1 messages

BuddyRequests:
1-1 connections
Can generate an event.


School:
    Users
    Classes
    Sesh
    Events
    Terms
    meta info

User:
    blocked_users
    blocked_by (may not be accesible on the client. we'll see.)
    buddies/requests/id
    buddies/list/id
    sesh/future/id
    sesh/past/id ?

Questions: 
    how do we deal with comment(event) or heart #?
    what happens when I delete my account?

At any given time, a user is subscribed to:
/user/me
    - profile
    - buddy relationships
    - news feed
    - inbox
/school/schid/class/chem123/
    - class chat
/school/schid/class/art32/
    - class chat
/school/schid/class/bio612/
    - class chat
/school/schid/class/bio612/
    - class chat
/school/schid/sesh/1234
    - sesh I'm going to


When Jenny Blocks Sam:
    - Sam can't see any of Jenny's events (activity), profile, sesh, etc.
    - Jenny can't see Sam, except:
        - Sam's profile (under "blocked" in her profile), so she can unblock
    - Jenny gets a warning if Sam is going to a sesh that she's going to.  Sam wouldn't know Jenny was going.


Home:
    get feed
        meService.news_feed_events
    get_more
        meService.news_feed_events (diff search) (later?)
    
    heart_story
        me.heart(event_id)
    load_detail
Inbox:
    load_list
    load_detail
Inbox message
    load_thread
    mark_read
    send_private_message
New message
    load_buddy_list
    send_private_message
Profile
    load_profile
    update_profile
    update_notifications
Settings: Password
    change_passord
Settings: Push Notifications
    update_notifications
Settings: Email Notifications
    update_notifications
Settings: About this version:
    version_info
Settings: Delete account


Buddies/Buddy Detail:
    load_buddies
    load_detail
    send_buddy_request
    cancel_buddy_request
    load_profile_detail
Study:
    create_group
    load_detail
    going_group
    leave_group
    send_chat_message
    end_group
    update_group
Hearts:
    load_buddies_hearts
    load_story_detail
    heart_story
Classes:
    load_list
    load_detail
    send_chat_message
    list_classmates
    load_study_list

Groundcontrol:
    See class
    see user (With all activity)
    see study groups at a school

    see global chat
    see global activity stream
    see global study groups
