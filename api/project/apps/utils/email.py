from utils.school_data import OVERRIDES


def get_school_key_from_email(email):
    try:
        email = email.split("@")[1]
        assert "." in email
        email = email.replace(".", "_")
        if email in OVERRIDES:
            return OVERRIDES[email]
        # print("returning %s" % email)
        return email

    except:
        pass
        # import traceback
        # traceback.print_exc()
