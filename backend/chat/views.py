# from django.shortcuts import render


# def index(request):
#     return render(request, "chat/index.html")


# def room(request, room_name):
#     return render(request, "chat/room.html", {"room_name": room_name})

from typing import Any
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

# from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserAccount
from accounts.serializers import ProfileSerializer
from chat.serializers import ChatModelSerializer
from chat.models import ChatModel
from django.views.generic import TemplateView

User = get_user_model()


class IndexView(TemplateView):
    template_name = "chat/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["users"] = UserAccount.objects.exclude(pk=self.request.user.pk)
        return context


# def index(request):
#     users = UserAccount.objects.exclude(email=request.user.email)
#     return render(request, "chat/index.html", context={"users": users})


class ChatPageView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, email, *args, **kwargs):
        user_obj = UserAccount.objects.get(email=email)  # request.user
        print("user_obj: ", user_obj)
        users = UserAccount.objects.exclude(email=request.user.email)
        print("users: ", users)

        if request.user.id > user_obj.id:
            thread_name = f"chat_{request.user.id}-{user_obj.id}"
        else:
            thread_name = f"chat_{user_obj.id}-{request.user.id}"
        message_objs = ChatModel.objects.filter(thread_name=thread_name)
        print("message_objs: ", message_objs)
        return render(
            request,
            "chat/main_chat.html",
            context={"user": user_obj, "users": users, "messages": message_objs},
        )


class ChatMessagesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, email, *args, **kwargs):
        user_obj = UserAccount.objects.get(email=email)  # request.user
        print("user_obj: ", user_obj)
        users = UserAccount.objects.exclude(email=request.user.email)
        print("users: ", users)

        if request.user.id > user_obj.id:
            thread_name = f"chat_{request.user.id}-{user_obj.id}"
        else:
            thread_name = f"chat_{user_obj.id}-{request.user.id}"
        message_objs = ChatModel.objects.filter(thread_name=thread_name)
        print("message_objs: ", message_objs)
        serializer = ChatModelSerializer(message_objs, many=True)
        return Response(serializer.data)


# class MyContactsApiView(ListAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ProfileSerializer

#     def get_queryset(self):
#         print("Getting contacts")
#         user_id = self.request.user.id
#         regex = f"chat_({user_id}-\d+|\d+-{user_id})"

#         ChatModel.objects.filter(thread_name__regex=regex)
#         return None

#     def get(self, request, *args, **kwargs):
#         print("**************************************************")
#         print("Get request triggered on MyContactsApiView")
#         print("**************************************************")
#         return super().get(request, *args, **kwargs)
