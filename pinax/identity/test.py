from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import (
    Client as TestClient,
    FakePayload,
)
from django.utils import six
from django.utils.encoding import force_bytes, force_str
from django.utils.six.moves.urllib.parse import urlparse

from oidc_provider.models import Client


class TokenizingClient(TestClient):
    """
    If `self.token` is present, sets "BEARER" header with access token.
    """

    def generic(self, method, path, data='',
                content_type='application/octet-stream', secure=False,
                **extra):
        """Constructs an arbitrary HTTP request."""
        parsed = urlparse(force_str(path))
        data = force_bytes(data, settings.DEFAULT_CHARSET)
        r = {
            'PATH_INFO': self._get_path(parsed),
            'REQUEST_METHOD': str(method),
            'SERVER_PORT': str('443') if secure else str('80'),
            'wsgi.url_scheme': str('https') if secure else str('http'),
        }
        if data:
            r.update({
                'CONTENT_LENGTH': len(data),
                'CONTENT_TYPE': str(content_type),
                'wsgi.input': FakePayload(data),
            })

        if hasattr(self, 'token'):
            r.update({'HTTP_AUTHORIZATION': "Bearer {}".format(self.token.access_token)})

        r.update(extra)
        # If QUERY_STRING is absent or empty, we want to extract it from the URL.
        if not r.get('QUERY_STRING'):
            query_string = force_bytes(parsed[4])
            # WSGI requires latin-1 encoded strings. See get_path_info().
            if six.PY3:
                query_string = query_string.decode('iso-8859-1')
            r['QUERY_STRING'] = query_string
        return self.request(**r)


class IdentityTestCase(TestCase):

    maxDiff = None
    client_class = TokenizingClient

    def setUp(self):
        super(IdentityTestCase, self).setUp()

        usermodel = get_user_model()

        # Create User for access token
        self.user_password = "changeme"
        self.login_user = usermodel.objects.create(
            username="loginuser",
            email="login_user@example.com",
            password=self.user_password,
            first_name="Login",
            last_name="User"
        )

        # Create access client
        self.oidc_client = Client.objects.create(
            name="oidc client",
            client_type="public",
            client_id="000001",
            response_type="id_token token",
        )

    def tokenize_url(self, url):
        if "?" in url:
            return "{}&access_token={}".format(url, self.token.access_token)
        else:
            return "{}?access_token={}".format(url, self.token.access_token)
