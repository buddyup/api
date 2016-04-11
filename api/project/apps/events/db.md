Data flow:

## Event flow

1. `POST` to `/api/event/`, with data like:
    
    ```json
    {
        "uid": "1231345",
        "request_time": "1231345",
        "type": "update_profile",
        "data": {
            "first_name": "Bar",
        },
        "signature": "12315334",
    }
    ```

    All posts are atomic, and self-contained.


2. Check JWT in header vs User ID in request.
3. Check signature (signed w/ JWT)

    - If either fails, return 401/3

4. Send save to event table log to celery

5. Send action to celery (full data blob)
    
    Check last_event table, write at completion (atomic w/ other write)

       - User
       - event_type
       - relevant_id (optional)
       - last_modified
       - create_or_update


7. Return response (200, success)
8. Client is authorized to do local modifications to data. (Except chat?)


## Writes

- Backend makes sure all nodes are right.
- If front touches the db,:
    1. responsible for making sure it's right
    2. must set last_modified for the node
    3. must make change as an atomic thing.
- When back makes changes
    1. Checks most specific last_modified node.
    2. If modified >= request_time, don't make changes.

## Reads

Reads are exclusively through Firebase, and limited by Firebase access rules based on userid (`uid`).

## Components

Data stores:

- Firebase  (Canonical data source)
- Postgres DB  (Logs, aggregation, analytics)

Application code:

- Django Views - handle events, authentication.
- Celery tasks - do writing to firebase and logs
- Angular Client-side app - user-facing app, does reads, sends events to django API, writes to select nodes (chat).


=======
Tests:
- Custom python test to ensure that bu.user.api has the same methods as the backend user.api.
- Blaze rules.yml inline tests for schema validity in firebase
- Unit tests on backend methods
- Unit tests on angular code, in complex cases
- e2e test for user to set up an account, add a couple classes, type in chat, add a buddy (get a buddy request), start a study group, and have that stuff show up in home.




TODOS: 

- Need to figure out expiration on JWT
- Make sure db supports all events, also last visit to chat (for what's happened since)
