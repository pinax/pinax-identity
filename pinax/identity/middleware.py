from oidc_provider.lib.utils.oauth2 import extract_access_token
from oidc_provider.models import Token

from django.contrib import auth
from django.utils.functional import SimpleLazyObject


class AuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = extract_access_token(request)
        try:
            token = Token.objects.get(access_token=access_token)
        except Token.DoesNotExist:
            self.unauthenticated(request)
        else:
            if not token.has_expired():
                self.authenticated(request, token)
            else:
                self.unauthenticated(request)
        return self.get_response(request)

    def unauthenticated(self, request):
        request.token = None
        request.user = SimpleLazyObject(lambda: auth.get_user(request))

    def authenticated(self, request, token):
        request.token = token
        request.user = token.user
