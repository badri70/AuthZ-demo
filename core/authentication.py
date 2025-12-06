from rest_framework.exceptions import AuthenticationFailed
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from core.utils import decode_jwt


class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(" ")
            if prefix.lower() != "bearer":
                raise AuthenticationFailed("Invalid token prefix")
        except ValueError:
            raise AuthenticationFailed("Invalid authorization header format")

        decoded_payload = decode_jwt(token)
        if not decoded_payload:
            raise AuthenticationFailed("Invalid or expired token")

        try:
            user = User.objects.get(id=decoded_payload["user_id"])
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return (user, None)