from oidc_provider.lib.utils.oauth2 import extract_access_token
from oidc_provider.models import Token

from pinax.api.exceptions import AuthenticationFailed


class TokenAuthentication(object):

    def authenticate(self, request):
        access_token = extract_access_token(request)
        try:
            token = Token.objects.get(access_token=access_token)
        except Token.DoesNotExist:
            raise AuthenticationFailed("invalid_token")
        if token.has_expired():
            raise AuthenticationFailed("invalid_token")
        request.token = token  # not an ideal side-affect, but required for now.
        return token
