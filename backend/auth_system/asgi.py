# import os
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from django.core.asgi import get_asgi_application
# from rest_framework_simplejwt.authentication import JWTAuthentication

# from chat.channels_middleware import JWTWebsocketMiddleware
# from chat.routing import websocket_urlpatterns

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auth_system.settings")
# django_asgi_app = get_asgi_application()


# application = ProtocolTypeRouter(
#     {
#         "http": django_asgi_app,
#         "websocket": JWTWebsocketMiddleware(
#             AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
#         ),
#     }
# )


import os
import django

from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()


# from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter

# from channels.auth import AuthMiddlewareStack


# from channels.security.websocket import AllowedHostsOriginValidator
from chat.channels_middleware import JWTWebsocketMiddleware
from chat.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auth_system.settings")
django.setup()
# Doc..........................


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # "websocket": AllowedHostsOriginValidator(
        #     AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        # ),
        "websocket": JWTWebsocketMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
