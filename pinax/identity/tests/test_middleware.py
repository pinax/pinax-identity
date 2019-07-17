import datetime
import pytz

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse

from oidc_provider.models import Token

from ..test import IdentityTestCase


class MiddlewareTestCase(IdentityTestCase):

    def setUp(self):
        super(MiddlewareTestCase, self).setUp()
        self.home_url = reverse("home")

    def test_anonymous(self):
        """
        Ensure request with no token results in response.context user==AnonymousUser
        """
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        user = response.context["user"]
        self.assertTrue(isinstance(user, AnonymousUser))

    def test_authenticated(self):
        """
        Ensure request with valid token results in response.context user==AuthUser
        """
        # Create valid access token
        self.token = Token.objects.create(
            user=self.login_user,
            client=self.oidc_client,
            expires_at=datetime.datetime(year=2100, month=1, day=1, tzinfo=pytz.utc),
            access_token="690c5505b06e44d4bf2215a4413c3b6b",
            _id_token="thisistheidtoken"
        )
        self.client.token = self.token

        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        user = response.context["user"]
        self.assertFalse(isinstance(user, AnonymousUser))
        self.assertTrue(isinstance(user, get_user_model()))

    def test_expired_token(self):
        """
        Ensure request with expired token results in response.context user==AnonymousUser
        """
        # Create expired access token
        self.token = Token.objects.create(
            user=self.login_user,
            client=self.oidc_client,
            expires_at=datetime.datetime(year=2000, month=1, day=1, tzinfo=pytz.utc),
            access_token="690c5505b06e44d4bf2215a4413c3b6b",
            _id_token="thisistheidtoken"
        )
        self.client.token = self.token

        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        user = response.context["user"]
        self.assertTrue(isinstance(user, AnonymousUser))
