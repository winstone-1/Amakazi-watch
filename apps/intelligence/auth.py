from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKey


class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        key = request.headers.get("X-API-Key")
        if not key:
            return None

        try:
            api_key = APIKey.objects.get(key=key, is_active=True)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid or inactive API key")

        if not api_key.is_within_limit():
            raise AuthenticationFailed(
                f"API key limit reached ({api_key.call_limit} calls/month). Upgrade your plan."
            )

        api_key.increment()
        return (api_key.user, api_key)
