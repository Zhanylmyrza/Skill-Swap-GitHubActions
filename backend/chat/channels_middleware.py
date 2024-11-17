from channels.middleware import BaseMiddleware
from rest_framework.exceptions import AuthenticationFailed
from django.db import close_old_connections
from channels.db import database_sync_to_async


# from accounts.tokenauthentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class JWTWebsocketMiddleware(BaseMiddleware):

    authentication = JWTAuthentication()

    async def __call__(self, scope, receive, send):

        print("Authentication Started")
        close_old_connections()

        query_string = scope.get("query_string", b"").decode("utf-8")
        print("query_string:", query_string)

        query_parameters = dict(qp.split("=") for qp in query_string.split("&"))
        token = query_parameters.get("token", None)

        print("raw_token:", token)
        if token is None:
            await send({"type": "websocket.close", "code": 4000})

        # Bizdiki
        try:
            validated_token = self.authentication.get_validated_token(token)

            user = await self.get_user(validated_token)

            print("user:", user)

            if user is not None:
                scope["user"] = user
            else:
                await send({"type": "websocket.close", "code": 4000})

            return await super().__call__(scope, receive, send)

        except InvalidToken:
            await send({"type": "websocket.close", "code": 4000})

    @database_sync_to_async
    def get_user(self, validated_token):
        return self.authentication.get_user(validated_token)
        # authentication = JWTAuthentication()
        # try:
        #     user = await authentication.authenticate_websocket(scope, token)
        #     if user is not None:
        #         scope["user"] = user
        #     else:
        #         await send({"type": "websocket.close", "code": 4000})
        #     return await super().__call__(scope, receive, send)
        # except AuthenticationFailed:
        #     await send({"type": "websocket.close", "code": 4002})
