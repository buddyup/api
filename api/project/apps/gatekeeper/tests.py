import json


from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.test import TestCase

from gatekeeper.models import User
from utils.factory import Factory


@override_settings(FIREBASE_KEY="1234")
class AuthenticationTests(TestCase):

    # def test_returns_valid_tokens_for_good_login(self):
    #     user, password = Factory.user(email="%s@buddyup.org" % Factory.rand_name().lower())
    #     response = self.client.post(
    #         reverse(
    #             'gatekeeper:authenticate',
    #         ),
    #         json.dumps({
    #             'email': user.email,
    #             'password': password,
    #         }),
    #         'json',
    #         HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    #     )
    #     json_string = response.content.decode('utf-8')
    #     response_data = json.loads(json_string)
    #     # Stale user object. :/
    #     user = User.objects.get(pk=user.pk)
    #     self.assertEquals(response_data["success"], True)
    #     self.assertEquals(response_data["api_jwt"], user.api_jwt)
    #     # self.assertEquals(response_data["fire_jwt"], user.fire_jwt)
    #     self.assertEquals(response_data["must_reset_password"], user.must_reset_password)

    def test_returns_success_false(self):
        response = self.client.post(
            reverse(
                'gatekeeper:authenticate',
            ),
            json.dumps({
                'email': 'me@example.com',
                'password': 'abc123',
            }),
            'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        json_string = response.content.decode('utf-8')
        response_data = json.loads(json_string)

        self.assertEquals(response_data["success"], False)
