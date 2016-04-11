# Run on server in case of weird firebase down missing buids.
import time
import datetime
from utils.email import get_school_key_from_email
from utils.school_data import school_data
from events.tasks import firebase_put, firebase_post
from gatekeeper.models import User


for user in User.objects.filter(buid=None):
    school_key = get_school_key_from_email(user.email)
    structure = user.scaffold_data
    structure["schools"] = {
        "%s" % (school_key,): {
            "id": school_key,
            "name": school_data[school_key]["name"],
        }
    }
    now = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
    structure["public"]["signed_up_at"] = now
    structure["public"]["buid"] = user.buid
    resp_json = firebase_post("/users/", structure)
    user.buid = resp_json["name"]
    user.save()
