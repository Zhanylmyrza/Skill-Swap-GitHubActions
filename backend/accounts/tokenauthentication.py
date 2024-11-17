import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime
from channels.db import database_sync_to_async

from accounts.models import UserAccount


User = get_user_model()


class JWTAuthentication(BaseAuthentication):

    def verify_token(self, payload):
        if "exp" not in payload:
            raise InvalidTokenError("Token has no expiration")

        exp_timestamp = payload["exp"]
        current_timestamp = datetime.utcnow().timestamp()

        if current_timestamp > exp_timestamp:
            raise ExpiredSignatureError("Token has expired")

    def extract_token(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("JWT "):
            return auth_header.split(" ")[1]
        return None

    @database_sync_to_async
    def authenticate_websocket(self, scope, token):
        try:

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print("paaaaaaaaaaaaaaaaaaaayload: ", payload)

            self.verify_token(payload=payload)

            email = payload["user_id"]
            print("teper email : ", email)
            user = UserAccount.objects.get(email=email)
            return user
        except (InvalidTokenError, ExpiredSignatureError, User.DoesNotExist):
            raise AuthenticationFailed("Invalid Token")
