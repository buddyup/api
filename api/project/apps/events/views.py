import random
import datetime
import json

from django.core.cache import cache
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from annoying.decorators import render_to, ajax_request

from gatekeeper.models import User
from events.tasks import handle_event


@ajax_request
@csrf_exempt
def event(request):
    # TODO: Authenticate the event from headers
    # Hand it off to the background processors.
    resp = {
        "success": False,
    }

    try:
        data = None
        if request.body:
            data = json.loads(request.body.decode('utf-8'))
            if (
                "key" in data and
                User.objects.filter(api_jwt_cached=str(data["key"])).count() == 1
            ):
                handle_event.delay(data)
                print("handed off")
                resp["success"] = True
            else:
                print("invalid request")
                print(data)
    except:
        import traceback
        traceback.print_exc()

    return resp


@ajax_request
@csrf_exempt
def speed(request):
    # Random speed test.  Hit the db and cache.
    u = User.objects.all().order_by("-pk")[0]
    u.email

    cache.set("speed", datetime.datetime.now())
    cache.get("speed")

    return {"success": True}
