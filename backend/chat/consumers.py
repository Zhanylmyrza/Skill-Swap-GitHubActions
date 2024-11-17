import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import UserAccount
from chat.models import ChatModel, UserProfileModel, ChatNotification

# from django.contrib.auth.models import User


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope["user"].id
        print("my_id: ", my_id)
        other_user_id = self.scope["url_route"]["kwargs"]["room_name"]
        print("other_user_id.......: ", other_user_id)

        if other_user_id.isdigit():
            other_user_id = int(other_user_id)
            print("Filtered other_user_id: ", other_user_id)

            self.scope["receiver"] = other_user_id
            if int(my_id) > int(other_user_id):
                self.room_name = f"{my_id}-{other_user_id}"
            else:
                self.room_name = f"{other_user_id}-{my_id}"

            self.room_group_name = "chat_%s" % self.room_name
            print(
                "personalChatConsumer_____ self.room_group_name >", self.room_group_name
            )

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        else:
            print("Value of other_user_id is not numeric.")

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        print("data receive_________: ", data)

        if "message" in data:
            message = data["message"]
            username = self.scope["user"].email
            receiver = data["receiver"]
            print("Received message:", message)
            print("Received username:", username)
            print("Received receiver:", receiver)

            await self.save_message(username, self.room_group_name, message, receiver)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": username,
                },
            )
        else:
            print("Received data type:", data["type"])

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(
            text_data=json.dumps({"message": message, "username": username})
        )

    async def disconnect(self, code):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def save_message(self, username, thread_name, message, receiver):
        chat_obj = ChatModel.objects.create(
            sender=username, message=message, thread_name=thread_name
        )
        other_user_id = self.scope["url_route"]["kwargs"]["room_name"]
        get_user = UserAccount.objects.get(id=other_user_id)
        if receiver == get_user.email:
            ChatNotification.objects.create(chat=chat_obj, user=get_user)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("I AM CONECTING NOTIFICATION ")
        my_id = self.scope["user"].id

        print("inside notification my_id: ", my_id)

        self.room_group_name = f"{my_id}"
        print("self.room_group_name:___________", self.room_group_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        print("I AM DISCONNECTED NOTIFICATION")
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_notification(self, event):
        print("I AM SENDING NOTIFICATION ")
        data = json.loads(event.get("value"))
        print("send_notification -> data -> ", data)
        count = data["count"]
        print("send_notification -> count ->", count)
        await self.send(text_data=json.dumps({"count": count}))


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        print(user)
        print("I AM  CONECTING ONLINE STATUS ")
        self.room_group_name = "user"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        print("I AM RECIEVING ONLINE STATUS ")
        data = json.loads(text_data)
        username = data["username"]
        connection_type = data["type"]
        print("connection_type oooooooooooonline:", connection_type)
        await self.change_online_status(username, connection_type)

    async def send_onlineStatus(self, event):
        print("I AM SENDING ONLINE STATUS ")
        data = json.loads(event.get("value"))
        username = data["username"]
        online_status = data["status"]
        await self.send(
            text_data=json.dumps({"username": username, "online_status": online_status})
        )

    async def disconnect(self, message):
        print("I AM DISCONECTING ONLINE STATUS ")
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def change_online_status(self, username, c_type):
        print("I AM CHANGING ONLINE STATUS")
        user = UserAccount.objects.get(username=username)
        userprofile = UserProfileModel.objects.get(user=user)
        if c_type == "open":
            userprofile.online_status = True
            userprofile.save()
        else:
            userprofile.online_status = False
            userprofile.save()


# import json
# from channels.generic.websocket import AsyncWebsocketConsumer


# class PersonalChatConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         request_user = self.scope["user"]
#         print(request_user, "USER")
#         if request_user.is_authenticated:
#             chat_with_user = self.scope["url_route"]["kwargs"]["id"]
#             user_ids = [int(request_user.id), int(chat_with_user)]
#             user_ids = sorted(user_ids)
#             self.room_group_name = f"chat_{request_user.id}"
#             print("room_group_name: ", self.room_group_name)
#             await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#             print("Point A")
#             await self.accept()
#             print("Point A")
#             # request_user.is_online = True
#             # request_user.save()
#         else:
#             await self.close()

#     async def receive(self, text_data=None, bytes_data=None):
#         request_user = self.scope["user"]
#         data = json.loads(text_data)
#         message = data["message"]
#         recipient = data["recipient"]
#         await self.channel_layer.group_send(
#             f"chat_{recipient}",
#             {
#                 "type": "chat_message",
#                 "message": message,
#                 "sender": request_user.id,
#             },
#         )

#     async def disconnect(self, code):
#         user = self.scope["user"]
#         self.channel_layer.group_discard(self.room_group_name, self.channel_name)
#         user.is_online = False
#         user.save()

#     async def chat_message(self, event):
#         message = event["message"]
#         sender = event["sender"]
#         await self.send(text_data=json.dumps({"message": message, "sender": sender}))
