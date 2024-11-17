from django.apps import AppConfig
from rest_framework_simplejwt.settings import api_settings


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"


# def my_jwt_payload_handler(user):
#     print("my_jwt_payload_handler called!")
#     payload = api_settings.JWT_PAYLOAD_HANDLER(user)
#     payload["email"] = user.email
#     payload["id"] = user.id
#     return payload
